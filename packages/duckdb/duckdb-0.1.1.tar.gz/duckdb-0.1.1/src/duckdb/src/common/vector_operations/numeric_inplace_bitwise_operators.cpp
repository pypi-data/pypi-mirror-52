//===--------------------------------------------------------------------===//
// numeric_inplace_operators.cpp
// Description: This file contains the implementation of numeric inplace
// bitwise ops: ^= &= |= >>= <<=
//===--------------------------------------------------------------------===//

#include "common/operator/numeric_inplace_bitwise_operators.hpp"

#include "common/vector_operations/inplace_loops.hpp"
#include "common/vector_operations/vector_operations.hpp"

using namespace duckdb;
using namespace std;

template <class OP> static void templated_inplace_bitwise_operation(Vector &result, Vector &input) {
	INPLACE_TYPE_CHECK(input, result);
	// the inplace loops take the result as the last parameter
	switch (input.type) {
	case TypeId::TINYINT:
		templated_inplace_loop<int8_t, int8_t, OP>(input, result);
		break;
	case TypeId::SMALLINT:
		templated_inplace_loop<int16_t, int16_t, OP>(input, result);
		break;
	case TypeId::INTEGER:
		templated_inplace_loop<int32_t, int32_t, OP>(input, result);
		break;
	case TypeId::BIGINT:
		templated_inplace_loop<int64_t, int64_t, OP>(input, result);
		break;
	case TypeId::HASH:
		templated_inplace_loop<uint64_t, uint64_t, OP>(input, result);
		break;
	default:
		throw InvalidTypeException(input.type, "Invalid type for addition");
	}
}

//===--------------------------------------------------------------------===//
// In-Place Bitwise XOR
//===--------------------------------------------------------------------===//
// left ^= right
void VectorOperations::BitwiseXORInPlace(Vector &result, Vector &input) {
	templated_inplace_bitwise_operation<duckdb::BitwiseXORInPlace>(result, input);
}
