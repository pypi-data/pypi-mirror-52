#include "parser/statement/update_statement.hpp"
#include "planner/binder.hpp"
#include "planner/expression/bound_default_expression.hpp"
#include "planner/expression_binder/update_binder.hpp"
#include "planner/expression_binder/where_binder.hpp"
#include "planner/statement/bound_update_statement.hpp"
#include "planner/tableref/bound_basetableref.hpp"
#include "planner/constraints/bound_check_constraint.hpp"
#include "parser/expression/columnref_expression.hpp"
#include "storage/data_table.hpp"

using namespace duckdb;
using namespace std;

static void BindExtraColumns(TableCatalogEntry &table, Binder &binder, ClientContext &context,
                             BoundUpdateStatement &result, unordered_set<column_t> &bound_columns) {
	if (bound_columns.size() <= 1) {
		return;
	}
	index_t found_column_count = 0;
	unordered_set<index_t> found_columns;
	for (index_t i = 0; i < result.column_ids.size(); i++) {
		if (bound_columns.find(result.column_ids[i]) != bound_columns.end()) {
			// this column is referenced in the CHECK constraint
			found_column_count++;
			found_columns.insert(result.column_ids[i]);
		}
	}
	if (found_column_count > 0 && found_column_count != bound_columns.size()) {
		// columns in this CHECK constraint were referenced, but not all were part of the UPDATE
		// add them to the scan and update set
		for (auto &check_column_id : bound_columns) {
			if (found_columns.find(check_column_id) != found_columns.end()) {
				// column is already projected
				continue;
			}
			// column is not projected yet: project it by adding the clause "i=i" to the set of updated columns
			result.column_ids.push_back(check_column_id);
			UpdateBinder update_binder(binder, context);
			auto &column = table.columns[check_column_id];
			update_binder.target_type = column.type;
			auto unbound_expr = make_unique_base<ParsedExpression, ColumnRefExpression>(column.name, table.name);
			auto bound_expr = update_binder.Bind(unbound_expr);
			result.expressions.push_back(move(bound_expr));
		}
	}
}

static void BindUpdateConstraints(TableCatalogEntry &table, Binder &binder, ClientContext &context,
                                  BoundUpdateStatement &result) {
	// check the constraints and indexes of the table to see if we need to project any additional columns
	// we do this for indexes with multiple columns and CHECK constraints in the UPDATE clause
	// suppose we have a constraint CHECK(i + j < 10); now we need both i and j to check the constraint
	// if we are only updating one of the two columns we add the other one to the UPDATE set
	// with a "useless" update (i.e. i=i) so we can verify that the CHECK constraint is not violated
	for (auto &constraint : table.bound_constraints) {
		if (constraint->type == ConstraintType::CHECK) {
			auto &check = *reinterpret_cast<BoundCheckConstraint *>(constraint.get());
			// check constraint! check if we need to add any extra columns to the UPDATE clause
			BindExtraColumns(table, binder, context, result, check.bound_columns);
		}
	}
	// do the same for all the indexes with multiple columns
	for (auto &index : table.storage->indexes) {
		BindExtraColumns(table, binder, context, result, index->column_id_set);
	}
}

unique_ptr<BoundSQLStatement> Binder::Bind(UpdateStatement &stmt) {
	auto result = make_unique<BoundUpdateStatement>();
	// visit the table reference
	result->table = Bind(*stmt.table);
	if (result->table->type != TableReferenceType::BASE_TABLE) {
		throw BinderException("Can only update base table!");
	}
	auto table = ((BoundBaseTableRef &)*result->table).table;
	result->proj_index = GenerateTableIndex();
	// project any additional columns required for the condition/expressions
	if (stmt.condition) {
		WhereBinder binder(*this, context);
		result->condition = binder.Bind(stmt.condition);
	}
	assert(stmt.columns.size() == stmt.expressions.size());
	for (index_t i = 0; i < stmt.columns.size(); i++) {
		auto &colname = stmt.columns[i];
		auto &expr = stmt.expressions[i];
		if (!table->ColumnExists(colname)) {
			throw BinderException("Referenced update column %s not found in table!", colname.c_str());
		}
		auto &column = table->GetColumn(colname);
		result->column_ids.push_back(column.oid);

		if (expr->type == ExpressionType::VALUE_DEFAULT) {
			result->expressions.push_back(
			    make_unique<BoundDefaultExpression>(GetInternalType(column.type), column.type));
		} else {
			UpdateBinder binder(*this, context);
			binder.target_type = column.type;
			auto bound_expr = binder.Bind(expr);
			result->expressions.push_back(move(bound_expr));
		}
	}
	BindUpdateConstraints(*table, *this, context, *result);
	// bind the default values
	BindDefaultValues(table->columns, result->bound_defaults);
	return move(result);
}
