//===----------------------------------------------------------------------===//
//                         DuckDB
//
// optimizer/rule/conjunction_simplification.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "optimizer/rule.hpp"

namespace duckdb {

// The Conjunction Simplification rule rewrites conjunctions with a constant
class ConjunctionSimplificationRule : public Rule {
public:
	ConjunctionSimplificationRule(ExpressionRewriter &rewriter);

	unique_ptr<Expression> Apply(LogicalOperator &op, vector<Expression *> &bindings, bool &changes_made) override;
};

} // namespace duckdb
