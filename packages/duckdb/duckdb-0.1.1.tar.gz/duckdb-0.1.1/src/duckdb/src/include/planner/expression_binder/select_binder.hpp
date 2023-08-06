//===----------------------------------------------------------------------===//
//                         DuckDB
//
// planner/expression_binder/select_binder.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/unordered_map.hpp"
#include "parser/expression_map.hpp"
#include "planner/expression_binder.hpp"

namespace duckdb {
class BoundColumnRefExpression;
class WindowExpression;

class BoundSelectNode;

struct BoundGroupInformation {
	expression_map_t<index_t> map;
	unordered_map<string, index_t> alias_map;
	vector<SQLType> group_types;
};

//! The SELECT binder is responsible for binding an expression within the SELECT clause of a SQL statement
class SelectBinder : public ExpressionBinder {
public:
	SelectBinder(Binder &binder, ClientContext &context, BoundSelectNode &node, BoundGroupInformation &info);

protected:
	BindResult BindExpression(ParsedExpression &expr, index_t depth, bool root_expression = false) override;

	BindResult BindAggregate(FunctionExpression &expr, AggregateFunctionCatalogEntry *function, index_t depth) override;

	bool inside_window;

	BoundSelectNode &node;
	BoundGroupInformation &info;

protected:
	BindResult BindWindow(WindowExpression &expr, index_t depth);

	index_t TryBindGroup(ParsedExpression &expr, index_t depth);
	BindResult BindGroup(ParsedExpression &expr, index_t depth, index_t group_index);
};

} // namespace duckdb
