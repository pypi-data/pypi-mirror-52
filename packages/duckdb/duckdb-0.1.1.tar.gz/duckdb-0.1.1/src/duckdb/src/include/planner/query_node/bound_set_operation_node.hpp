//===----------------------------------------------------------------------===//
//                         DuckDB
//
// planner/query_node/bound_set_operation_node.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/enums/set_operation_type.hpp"
#include "planner/binder.hpp"
#include "planner/bound_query_node.hpp"

namespace duckdb {

//! Bound equivalent of SetOperationNode
class BoundSetOperationNode : public BoundQueryNode {
public:
	BoundSetOperationNode() : BoundQueryNode(QueryNodeType::SET_OPERATION_NODE) {
	}

	//! The type of set operation
	SetOperationType setop_type = SetOperationType::NONE;
	//! The left side of the set operation
	unique_ptr<BoundQueryNode> left;
	//! The right side of the set operation
	unique_ptr<BoundQueryNode> right;

	//! Index used by the set operation
	index_t setop_index;
	//! The binder used by the left side of the set operation
	unique_ptr<Binder> left_binder;
	//! The binder used by the right side of the set operation
	unique_ptr<Binder> right_binder;
};

}; // namespace duckdb
