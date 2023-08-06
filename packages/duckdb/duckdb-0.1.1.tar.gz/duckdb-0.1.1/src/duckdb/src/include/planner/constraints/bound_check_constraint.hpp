//===----------------------------------------------------------------------===//
//                         DuckDB
//
// planner/constraints/bound_check_constraint.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/exception.hpp"
#include "planner/bound_constraint.hpp"
#include "planner/expression.hpp"

namespace duckdb {

//! The CheckConstraint contains an expression that must evaluate to TRUE for
//! every row in a table
class BoundCheckConstraint : public BoundConstraint {
public:
	BoundCheckConstraint() : BoundConstraint(ConstraintType::CHECK) {
	}

	//! The expression
	unique_ptr<Expression> expression;
	//! The columns used by the CHECK constraint
	unordered_set<column_t> bound_columns;
};

} // namespace duckdb
