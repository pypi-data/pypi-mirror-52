#include "planner/binder.hpp"

#include "execution/expression_executor.hpp"
#include "parser/statement/list.hpp"
#include "planner/bound_query_node.hpp"
#include "planner/bound_sql_statement.hpp"
#include "planner/bound_tableref.hpp"
#include "planner/expression.hpp"
#include "planner/expression_binder/constant_binder.hpp"

using namespace duckdb;
using namespace std;

Binder::Binder(ClientContext &context, Binder *parent)
    : context(context), parent(!parent ? nullptr : (parent->parent ? parent->parent : parent)), bound_tables(0) {
	if (parent) {
		parameters = parent->parameters;
	}
}

unique_ptr<BoundSQLStatement> Binder::Bind(SQLStatement &statement) {
	switch (statement.type) {
	case StatementType::SELECT:
		return Bind((SelectStatement &)statement);
	case StatementType::INSERT:
		return Bind((InsertStatement &)statement);
	case StatementType::COPY:
		return Bind((CopyStatement &)statement);
	case StatementType::DELETE:
		return Bind((DeleteStatement &)statement);
	case StatementType::UPDATE:
		return Bind((UpdateStatement &)statement);
	case StatementType::ALTER:
		return Bind((AlterTableStatement &)statement);
	case StatementType::CREATE_TABLE:
		return Bind((CreateTableStatement &)statement);
	case StatementType::CREATE_VIEW:
		return Bind((CreateViewStatement &)statement);
	case StatementType::EXECUTE:
		return Bind((ExecuteStatement &)statement);
	default:
		assert(statement.type == StatementType::CREATE_INDEX);
		return Bind((CreateIndexStatement &)statement);
	}
}

static int64_t BindConstant(Binder &binder, ClientContext &context, string clause, unique_ptr<ParsedExpression> &expr) {
	ConstantBinder constant_binder(binder, context, clause);
	auto bound_expr = constant_binder.Bind(expr);
	Value value = ExpressionExecutor::EvaluateScalar(*bound_expr);
	if (!TypeIsNumeric(value.type)) {
		throw BinderException("LIMIT clause can only contain numeric constants!");
	}
	int64_t limit_value = value.GetNumericValue();
	if (limit_value < 0) {
		throw BinderException("LIMIT must not be negative");
	}
	return limit_value;
}

unique_ptr<BoundQueryNode> Binder::Bind(QueryNode &node) {
	unique_ptr<BoundQueryNode> result;
	switch (node.type) {
	case QueryNodeType::SELECT_NODE:
		result = Bind((SelectNode &)node);
		break;
	default:
		assert(node.type == QueryNodeType::SET_OPERATION_NODE);
		result = Bind((SetOperationNode &)node);
		break;
	}
	// DISTINCT ON select list
	result->select_distinct = node.select_distinct;
	// bind the limit nodes
	if (node.limit) {
		result->limit = BindConstant(*this, context, "LIMIT clause", node.limit);
		result->offset = 0;
	}
	if (node.offset) {
		result->offset = BindConstant(*this, context, "OFFSET clause", node.offset);
		if (!node.limit) {
			result->limit = std::numeric_limits<int64_t>::max();
		}
	}
	return result;
}

unique_ptr<BoundTableRef> Binder::Bind(TableRef &ref) {
	switch (ref.type) {
	case TableReferenceType::BASE_TABLE:
		return Bind((BaseTableRef &)ref);
	case TableReferenceType::CROSS_PRODUCT:
		return Bind((CrossProductRef &)ref);
	case TableReferenceType::JOIN:
		return Bind((JoinRef &)ref);
	case TableReferenceType::SUBQUERY:
		return Bind((SubqueryRef &)ref);
	default:
		assert(ref.type == TableReferenceType::TABLE_FUNCTION);
		return Bind((TableFunctionRef &)ref);
	}
}

void Binder::AddCTE(const string &name, QueryNode *cte) {
	assert(cte);
	assert(!name.empty());
	auto entry = CTE_bindings.find(name);
	if (entry != CTE_bindings.end()) {
		throw BinderException("Duplicate CTE \"%s\" in query!", name.c_str());
	}
	CTE_bindings[name] = cte;
}

unique_ptr<QueryNode> Binder::FindCTE(const string &name) {
	auto entry = CTE_bindings.find(name);
	if (entry == CTE_bindings.end()) {
		if (parent) {
			return parent->FindCTE(name);
		}
		return nullptr;
	}
	return entry->second->Copy();
}

index_t Binder::GenerateTableIndex() {
	if (parent) {
		return parent->GenerateTableIndex();
	}
	return bound_tables++;
}

void Binder::PushExpressionBinder(ExpressionBinder *binder) {
	GetActiveBinders().push_back(binder);
}

void Binder::PopExpressionBinder() {
	assert(HasActiveBinder());
	GetActiveBinders().pop_back();
}

void Binder::SetActiveBinder(ExpressionBinder *binder) {
	assert(HasActiveBinder());
	GetActiveBinders().back() = binder;
}

ExpressionBinder *Binder::GetActiveBinder() {
	return GetActiveBinders().back();
}

bool Binder::HasActiveBinder() {
	return GetActiveBinders().size() > 0;
}

vector<ExpressionBinder *> &Binder::GetActiveBinders() {
	if (parent) {
		return parent->GetActiveBinders();
	}
	return active_binders;
}

void Binder::MoveCorrelatedExpressions(Binder &other) {
	MergeCorrelatedColumns(other.correlated_columns);
	other.correlated_columns.clear();
}

void Binder::MergeCorrelatedColumns(vector<CorrelatedColumnInfo> &other) {
	for (index_t i = 0; i < other.size(); i++) {
		AddCorrelatedColumn(other[i]);
	}
}

void Binder::AddCorrelatedColumn(CorrelatedColumnInfo info) {
	// we only add correlated columns to the list if they are not already there
	if (std::find(correlated_columns.begin(), correlated_columns.end(), info) == correlated_columns.end()) {
		correlated_columns.push_back(info);
	}
}
