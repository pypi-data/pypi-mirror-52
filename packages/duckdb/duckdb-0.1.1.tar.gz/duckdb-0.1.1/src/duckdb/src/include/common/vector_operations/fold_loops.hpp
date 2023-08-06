//===----------------------------------------------------------------------===//
//                         DuckDB
//
// common/vector_operations/fold_loops.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/exception.hpp"
#include "common/types/vector.hpp"
#include "common/vector_operations/vector_operations.hpp"

namespace duckdb {

template <class LEFT_TYPE, class RESULT_TYPE, class OP, bool HAS_SEL_VECTOR>
static inline bool fold_loop_function(LEFT_TYPE *__restrict ldata, RESULT_TYPE *__restrict result, index_t count,
                                      sel_t *__restrict sel_vector, nullmask_t &nullmask) {
	ASSERT_RESTRICT(ldata, ldata + count, result, result + 1);
	if (nullmask.any()) {
		// skip null values in the operation
		index_t i = 0;
		// find the first null value
		for(; i < count; i++) {
			index_t index = HAS_SEL_VECTOR ? sel_vector[i] : i;
			if (!nullmask[index]) {
				*result = ldata[index];
				break;
			}
		}
		if (i == count) {
			return false;
		}
		// now perform the rest of the iteration
		for(i++; i < count; i++) {
			index_t index = HAS_SEL_VECTOR ? sel_vector[i] : i;
			if (!nullmask[index]) {
				*result = OP::Operation(ldata[index], *result);
			}
		}
	} else {
		// quick path: no NULL values
		*result = ldata[HAS_SEL_VECTOR ? sel_vector[0] : 0];
		for(index_t i = 1; i < count; i++) {
			*result = OP::Operation(ldata[HAS_SEL_VECTOR ? sel_vector[i] : i], *result);
		}
	}
	return true;
}

template <class LEFT_TYPE, class RESULT_TYPE, class OP> bool templated_unary_fold(Vector &input, RESULT_TYPE *result) {
	auto ldata = (LEFT_TYPE *)input.data;
	if (input.sel_vector) {
		return fold_loop_function<LEFT_TYPE, RESULT_TYPE, OP, true>(ldata, result, input.count, input.sel_vector, input.nullmask);
	} else {
		return fold_loop_function<LEFT_TYPE, RESULT_TYPE, OP, false>(ldata, result, input.count, input.sel_vector, input.nullmask);
	}
}

} // namespace duckdb
