#include "common/operator/comparison_operators.hpp"
#include "common/vector_operations/vector_operations.hpp"
#include "execution/nested_loop_join.hpp"

using namespace duckdb;
using namespace std;

template <class T, class OP> static void mark_join_templated(Vector &left, Vector &right, bool found_match[]) {
	auto ldata = (T *)left.data;
	auto rdata = (T *)right.data;
	VectorOperations::Exec(left, [&](index_t left_position, index_t k) {
		VectorOperations::Exec(right, [&](index_t right_position, index_t k) {
			if (OP::Operation(ldata[left_position], rdata[right_position])) {
				found_match[left_position] = true;
			}
		});
	});
}

template <class OP> static void mark_join_operator(Vector &left, Vector &right, bool found_match[]) {
	switch (left.type) {
	case TypeId::BOOLEAN:
	case TypeId::TINYINT:
		return mark_join_templated<int8_t, OP>(left, right, found_match);
	case TypeId::SMALLINT:
		return mark_join_templated<int16_t, OP>(left, right, found_match);
	case TypeId::INTEGER:
		return mark_join_templated<int32_t, OP>(left, right, found_match);
	case TypeId::BIGINT:
		return mark_join_templated<int64_t, OP>(left, right, found_match);
	case TypeId::FLOAT:
		return mark_join_templated<float, OP>(left, right, found_match);
	case TypeId::DOUBLE:
		return mark_join_templated<double, OP>(left, right, found_match);
	case TypeId::VARCHAR:
		return mark_join_templated<const char *, OP>(left, right, found_match);
	default:
		throw NotImplementedException("Unimplemented type for join!");
	}
}

static void mark_join(Vector &left, Vector &right, bool found_match[], ExpressionType comparison_type) {
	assert(left.type == right.type);
	switch (comparison_type) {
	case ExpressionType::COMPARE_EQUAL:
		return mark_join_operator<duckdb::Equals>(left, right, found_match);
	case ExpressionType::COMPARE_NOTEQUAL:
		return mark_join_operator<duckdb::NotEquals>(left, right, found_match);
	case ExpressionType::COMPARE_LESSTHAN:
		return mark_join_operator<duckdb::LessThan>(left, right, found_match);
	case ExpressionType::COMPARE_GREATERTHAN:
		return mark_join_operator<duckdb::GreaterThan>(left, right, found_match);
	case ExpressionType::COMPARE_LESSTHANOREQUALTO:
		return mark_join_operator<duckdb::LessThanEquals>(left, right, found_match);
	case ExpressionType::COMPARE_GREATERTHANOREQUALTO:
		return mark_join_operator<duckdb::GreaterThanEquals>(left, right, found_match);
	default:
		throw NotImplementedException("Unimplemented comparison type for join!");
	}
}

void NestedLoopJoinMark::Perform(DataChunk &left, ChunkCollection &right, bool found_match[],
                                 vector<JoinCondition> &conditions) {
	// initialize a new temporary selection vector for the left chunk
	// loop over all chunks in the RHS
	for (index_t chunk_idx = 0; chunk_idx < right.chunks.size(); chunk_idx++) {
		DataChunk &right_chunk = *right.chunks[chunk_idx];
		for (index_t i = 0; i < conditions.size(); i++) {
			mark_join(left.data[i], right_chunk.data[i], found_match, conditions[i].comparison);
		}
	}
}
