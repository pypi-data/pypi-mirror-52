//===----------------------------------------------------------------------===//
//                         DuckDB
//
// execution/operator/join/physical_join.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "execution/physical_operator.hpp"
#include "planner/operator/logical_comparison_join.hpp"

namespace duckdb {

//! PhysicalJoin represents the base class of the join operators
class PhysicalJoin : public PhysicalOperator {
public:
	PhysicalJoin(LogicalOperator &op, PhysicalOperatorType type, JoinType join_type);

	JoinType type;
};

void ConstructMarkJoinResult(DataChunk &join_keys, DataChunk &child, DataChunk &result, bool found_match[],
                             bool right_has_null);
} // namespace duckdb
