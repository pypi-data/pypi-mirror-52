#include "planner/expression/bound_reference_expression.hpp"

#include "common/serializer.hpp"
#include "common/types/hash.hpp"

using namespace duckdb;
using namespace std;

BoundReferenceExpression::BoundReferenceExpression(string alias, TypeId type, index_t index)
    : Expression(ExpressionType::BOUND_REF, ExpressionClass::BOUND_REF, type), index(index) {
	this->alias = alias;
}
BoundReferenceExpression::BoundReferenceExpression(TypeId type, index_t index)
    : BoundReferenceExpression(string(), type, index) {
}

string BoundReferenceExpression::ToString() const {
	return "#" + std::to_string(index);
}

bool BoundReferenceExpression::Equals(const BaseExpression *other_) const {
	if (!BaseExpression::Equals(other_)) {
		return false;
	}
	auto other = (BoundReferenceExpression *)other_;
	return other->index == index;
}

uint64_t BoundReferenceExpression::Hash() const {
	return CombineHash(Expression::Hash(), duckdb::Hash<index_t>(index));
}

unique_ptr<Expression> BoundReferenceExpression::Copy() {
	return make_unique<BoundReferenceExpression>(alias, return_type, index);
}
