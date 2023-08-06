#include "common/exception.hpp"
#include "parser/expression/columnref_expression.hpp"
#include "parser/expression/comparison_expression.hpp"
#include "parser/expression/conjunction_expression.hpp"
#include "parser/tableref/basetableref.hpp"
#include "parser/tableref/crossproductref.hpp"
#include "parser/tableref/joinref.hpp"
#include "parser/transformer.hpp"

using namespace duckdb;
using namespace postgres;
using namespace std;

static string get_tablename_union(TableRef *ref) {
	switch (ref->type) {
	case TableReferenceType::BASE_TABLE:
		if (ref->alias.size() > 0) {
			return ref->alias;
		}
		return ((BaseTableRef *)ref)->table_name;
	case TableReferenceType::SUBQUERY:
		assert(ref->alias.length() > 0);
		return ref->alias;
	default:
		throw ParserException("Cannot get table name for USING");
	}
}

unique_ptr<TableRef> Transformer::TransformJoin(JoinExpr *root) {
	auto result = make_unique<JoinRef>();
	switch (root->jointype) {
	case JOIN_INNER: {
		result->type = JoinType::INNER;
		break;
	}
	case JOIN_LEFT: {
		result->type = JoinType::LEFT;
		break;
	}
	case JOIN_FULL: {
		result->type = JoinType::OUTER;
		break;
	}
	case JOIN_RIGHT: {
		result->type = JoinType::RIGHT;
		break;
	}
	case JOIN_SEMI: {
		result->type = JoinType::SEMI;
		break;
	}
	default: {
		throw NotImplementedException("Join type %d not supported yet...\n", root->jointype);
	}
	}

	// Check the type of left arg and right arg before transform
	result->left = TransformTableRefNode(root->larg);
	result->right = TransformTableRefNode(root->rarg);

	if (root->usingClause && root->usingClause->length > 0) {
		// usingClause is a list of strings
		vector<string> using_column_names;
		for (auto node = root->usingClause->head; node != nullptr; node = node->next) {
			auto target = reinterpret_cast<Node *>(node->data.ptr_value);
			assert(target->type == T_String);
			auto column_name = string(reinterpret_cast<postgres::Value *>(target)->val.str);
			using_column_names.push_back(column_name);
		}
		assert(using_column_names.size() > 0);

		unique_ptr<ParsedExpression> join_condition = nullptr;
		for (auto column_name : using_column_names) {
			auto left_expr = make_unique<ColumnRefExpression>(column_name, get_tablename_union(result->left.get()));
			auto right_expr = make_unique<ColumnRefExpression>(column_name, get_tablename_union(result->right.get()));
			result->hidden_columns.insert(right_expr->table_name + "." + right_expr->column_name);
			auto comp_expr =
			    make_unique<ComparisonExpression>(ExpressionType::COMPARE_EQUAL, move(left_expr), move(right_expr));
			if (!join_condition) {
				join_condition = move(comp_expr);
			} else {
				join_condition = make_unique<ConjunctionExpression>(ExpressionType::CONJUNCTION_AND,
				                                                    move(join_condition), move(comp_expr));
			}
		}
		assert(join_condition != nullptr);
		result->condition = move(join_condition);
		return move(result);
	}

	if (!root->quals) { // CROSS PRODUCT
		auto cross = make_unique<CrossProductRef>();
		cross->left = move(result->left);
		cross->right = move(result->right);
		return move(cross);
	}

	result->condition = TransformExpression(root->quals);
	return move(result);
}
