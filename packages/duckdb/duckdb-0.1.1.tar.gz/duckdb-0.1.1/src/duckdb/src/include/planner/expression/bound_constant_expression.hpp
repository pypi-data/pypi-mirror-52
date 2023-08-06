//===----------------------------------------------------------------------===//
//                         DuckDB
//
// planner/expression/bound_constant_expression.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/types/value.hpp"
#include "planner/expression.hpp"

namespace duckdb {

class BoundConstantExpression : public Expression {
public:
	BoundConstantExpression(Value value);

	Value value;

public:
	string ToString() const override;

	bool Equals(const BaseExpression *other) const override;
	uint64_t Hash() const override;

	unique_ptr<Expression> Copy() override;
};
} // namespace duckdb
