#include "planner/expression/bound_columnref_expression.hpp"
#include "planner/logical_plan_generator.hpp"
#include "planner/operator/logical_filter.hpp"
#include "planner/operator/logical_get.hpp"
#include "planner/operator/logical_projection.hpp"
#include "planner/operator/logical_update.hpp"
#include "planner/statement/bound_update_statement.hpp"

using namespace duckdb;
using namespace std;

unique_ptr<LogicalOperator> LogicalPlanGenerator::CreatePlan(BoundUpdateStatement &stmt) {
	// we require row ids for the deletion
	require_row_id = true;
	// create the table scan
	auto root = CreatePlan(*stmt.table);
	assert(root->type == LogicalOperatorType::GET);

	auto &get = (LogicalGet &)*root;
	// create the filter (if any)
	if (stmt.condition) {
		PlanSubqueries(&stmt.condition, &root);
		auto filter = make_unique<LogicalFilter>(move(stmt.condition));
		filter->AddChild(move(root));
		root = move(filter);
	}
	// scan the table for the referenced columns in the update clause
	auto &table = get.table;
	vector<unique_ptr<Expression>> projection_expressions;
	for (index_t i = 0; i < stmt.expressions.size(); i++) {
		if (stmt.expressions[i]->type != ExpressionType::VALUE_DEFAULT) {
			// plan subqueries inside the expression
			PlanSubqueries(&stmt.expressions[i], &root);
			// move the expression into the LogicalProjection
			auto expression = move(stmt.expressions[i]);
			stmt.expressions[i] = make_unique<BoundColumnRefExpression>(
			    expression->return_type, ColumnBinding(stmt.proj_index, projection_expressions.size()));
			projection_expressions.push_back(move(expression));
		}
	}
	// add the row id column to the projection list
	projection_expressions.push_back(make_unique<BoundColumnRefExpression>(
	    TypeId::BIGINT, ColumnBinding(get.table_index, get.column_ids.size() - 1)));
	// now create the projection
	auto proj = make_unique<LogicalProjection>(stmt.proj_index, move(projection_expressions));
	proj->AddChild(move(root));

	// create the update node
	auto update = make_unique<LogicalUpdate>(table, stmt.column_ids, move(stmt.expressions), move(stmt.bound_defaults));
	update->AddChild(move(proj));
	return move(update);
}
