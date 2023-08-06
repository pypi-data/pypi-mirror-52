//===----------------------------------------------------------------------===//
//                         DuckDB
//
// planner/subquery/flatten_dependent_join.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/unordered_map.hpp"
#include "planner/binder.hpp"
#include "planner/column_binding_map.hpp"
#include "planner/logical_operator.hpp"

namespace duckdb {

//! The FlattenDependentJoins class is responsible for pushing the dependent join down into the plan to create a
//! flattened subquery
struct FlattenDependentJoins {
	FlattenDependentJoins(Binder &binder, const vector<CorrelatedColumnInfo> &correlated);

	//! Detects which Logical Operators have correlated expressions that they are dependent upon, filling the
	//! has_correlated_expressions map.
	bool DetectCorrelatedExpressions(LogicalOperator *op);

	//! Push the dependent join down a LogicalOperator
	unique_ptr<LogicalOperator> PushDownDependentJoin(unique_ptr<LogicalOperator> plan);

	Binder &binder;
	ColumnBinding base_binding;
	index_t delim_offset;
	index_t data_offset;
	unordered_map<LogicalOperator *, bool> has_correlated_expressions;
	column_binding_map_t<index_t> correlated_map;
	column_binding_map_t<index_t> replacement_map;
	const vector<CorrelatedColumnInfo> &correlated_columns;
	vector<TypeId> delim_types;

private:
	unique_ptr<LogicalOperator> PushDownDependentJoinInternal(unique_ptr<LogicalOperator> plan);
};

} // namespace duckdb
