//===----------------------------------------------------------------------===//
//                         DuckDB
//
// planner/operator/logical_limit.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "planner/logical_operator.hpp"

namespace duckdb {

//! LogicalLimit represents a LIMIT clause
class LogicalLimit : public LogicalOperator {
public:
	LogicalLimit(int64_t limit, int64_t offset)
	    : LogicalOperator(LogicalOperatorType::LIMIT), limit(limit), offset(offset) {
	}

	//! The maximum amount of elements to emit
	int64_t limit;
	//! The offset from the start to begin emitting elements
	int64_t offset;

protected:
	void ResolveTypes() override {
		types = children[0]->types;
	}
};
} // namespace duckdb
