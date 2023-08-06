#include "planner/expression.hpp"

#include "common/exception.hpp"
#include "common/types/hash.hpp"
#include "planner/expression_iterator.hpp"

using namespace duckdb;
using namespace std;

Expression::Expression(ExpressionType type, ExpressionClass expression_class, TypeId return_type)
    : BaseExpression(type, expression_class), return_type(return_type) {
}

bool Expression::IsAggregate() const {
	bool is_aggregate = false;
	ExpressionIterator::EnumerateChildren(*this, [&](const Expression &child) { is_aggregate |= child.IsAggregate(); });
	return is_aggregate;
}

bool Expression::IsWindow() const {
	bool is_window = false;
	ExpressionIterator::EnumerateChildren(*this, [&](const Expression &child) { is_window |= child.IsWindow(); });
	return is_window;
}

bool Expression::IsScalar() const {
	bool is_scalar = true;
	ExpressionIterator::EnumerateChildren(*this, [&](const Expression &child) {
		if (!child.IsScalar()) {
			is_scalar = false;
		}
	});
	return is_scalar;
}

bool Expression::IsFoldable() const {
	bool is_foldable = true;
	ExpressionIterator::EnumerateChildren(*this, [&](const Expression &child) {
		if (!child.IsFoldable()) {
			is_foldable = false;
		}
	});
	return is_foldable;
}

bool Expression::HasParameter() const {
	bool has_parameter = false;
	ExpressionIterator::EnumerateChildren(*this,
	                                      [&](const Expression &child) { has_parameter |= child.HasParameter(); });
	return has_parameter;
}

bool Expression::HasSubquery() const {
	bool has_subquery = false;
	ExpressionIterator::EnumerateChildren(*this, [&](const Expression &child) { has_subquery |= child.HasSubquery(); });
	return has_subquery;
}

uint64_t Expression::Hash() const {
	uint64_t hash = duckdb::Hash<uint32_t>((uint32_t)type);
	hash = CombineHash(hash, duckdb::Hash<uint32_t>((uint32_t)return_type));
	ExpressionIterator::EnumerateChildren(*this,
	                                      [&](const Expression &child) { hash = CombineHash(child.Hash(), hash); });
	return hash;
}
