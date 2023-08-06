//===--------------------------------------------------------------------===//
// gather.cpp
// Description: This file contains the implementation of the gather operators
//===--------------------------------------------------------------------===//

#include "common/exception.hpp"
#include "common/operator/constant_operators.hpp"
#include "common/types/null_value.hpp"
#include "common/vector_operations/vector_operations.hpp"

using namespace duckdb;
using namespace std;

struct GatherLoopSetNull {
	template <class T, class OP> static void Operation(Vector &src, Vector &result, index_t offset) {
		(void)offset;
		auto source = (T **)src.data;
		auto ldata = (T *)result.data;
		if (result.sel_vector) {
			VectorOperations::Exec(src, [&](index_t i, index_t k) {
				if (IsNullValue<T>(source[i][0])) {
					result.nullmask.set(result.sel_vector[k]);
				} else {
					ldata[result.sel_vector[k]] = OP::Operation(source[i][0], ldata[i]);
				}
			});
		} else {
			VectorOperations::Exec(src, [&](index_t i, index_t k) {
				if (IsNullValue<T>(source[i][0])) {
					result.nullmask.set(k);
				} else {
					ldata[k] = OP::Operation(source[i][0], ldata[i]);
				}
			});
		}
	}
};

struct GatherLoopIgnoreNull {
	template <class T, class OP> static void Operation(Vector &src, Vector &result, index_t offset) {
		(void)offset;
		auto source = (T **)src.data;
		auto ldata = (T *)result.data;
		if (result.sel_vector) {
			VectorOperations::Exec(src, [&](index_t i, index_t k) {
				ldata[result.sel_vector[k]] = OP::Operation(source[i][0], ldata[i]);
			});
		} else {
			VectorOperations::Exec(src,
			                       [&](index_t i, index_t k) { ldata[k] = OP::Operation(source[i][0], ldata[i]); });
		}
	}
};

template <class LOOP, class OP> static void generic_gather_loop(Vector &source, Vector &dest, index_t offset = 0) {
	if (source.type != TypeId::POINTER) {
		throw InvalidTypeException(source.type, "Cannot gather from non-pointer type!");
	}
	switch (dest.type) {
	case TypeId::BOOLEAN:
	case TypeId::TINYINT:
		LOOP::template Operation<int8_t, OP>(source, dest, offset);
		break;
	case TypeId::SMALLINT:
		LOOP::template Operation<int16_t, OP>(source, dest, offset);
		break;
	case TypeId::INTEGER:
		LOOP::template Operation<int32_t, OP>(source, dest, offset);
		break;
	case TypeId::BIGINT:
		LOOP::template Operation<int64_t, OP>(source, dest, offset);
		break;
	case TypeId::FLOAT:
		LOOP::template Operation<float, OP>(source, dest, offset);
		break;
	case TypeId::DOUBLE:
		LOOP::template Operation<double, OP>(source, dest, offset);
		break;
	case TypeId::POINTER:
		LOOP::template Operation<uint64_t, OP>(source, dest, offset);
		break;
	case TypeId::VARCHAR:
		LOOP::template Operation<char *, OP>(source, dest, offset);
		break;
	default:
		throw NotImplementedException("Unimplemented type for gather");
	}
}

void VectorOperations::Gather::Set(Vector &source, Vector &dest, bool set_null, index_t offset) {
	if (set_null) {
		generic_gather_loop<GatherLoopSetNull, PickLeft>(source, dest, offset);
	} else {
		generic_gather_loop<GatherLoopIgnoreNull, PickLeft>(source, dest, offset);
	}
	dest.count = source.count;
}

struct GatherLoopAppendNull {
	template <class T, class OP> static void Operation(Vector &src, Vector &result, index_t offset) {
		(void)offset;
		auto source = (data_ptr_t *)src.data;
		auto ldata = (T *)result.data;
		VectorOperations::Exec(src, [&](index_t i, index_t k) {
			T val = *((T *)(source[i] + offset));
			result.nullmask[result.count] = IsNullValue<T>(val);
			ldata[result.count] = *((T *)(source[i] + offset));
			result.count++;
		});
	}
};

struct GatherLoopAppend {
	template <class T, class OP> static void Operation(Vector &src, Vector &result, index_t offset) {
		(void)offset;
		auto source = (data_t **)src.data;
		auto ldata = (T *)result.data;
		VectorOperations::Exec(src,
		                       [&](index_t i, index_t k) { ldata[result.count++] = *((T *)(source[i] + offset)); });
	}
};

void VectorOperations::Gather::Append(Vector &source, Vector &dest, index_t offset, bool set_null) {
	// neither source nor dest are allowed to have a selection vector
	assert(!source.sel_vector && !dest.sel_vector);
	assert(dest.count + source.count <= STANDARD_VECTOR_SIZE);
	if (set_null) {
		generic_gather_loop<GatherLoopAppendNull, PickLeft>(source, dest, offset);
	} else {
		generic_gather_loop<GatherLoopAppend, PickLeft>(source, dest, offset);
	}
}
