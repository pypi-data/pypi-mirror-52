#include "common/types/null_value.hpp"

#include "common/exception.hpp"

#include <cstring>

using namespace std;

namespace duckdb {

bool IsNullValue(data_ptr_t ptr, TypeId type) {
	data_t data[100];
	SetNullValue(data, type);
	return memcmp(ptr, data, GetTypeIdSize(type)) == 0;
}

//! Writes NullValue<T> value of a specific type to a memory address
void SetNullValue(data_ptr_t ptr, TypeId type) {
	switch (type) {
	case TypeId::BOOLEAN:
	case TypeId::TINYINT:
		*((int8_t *)ptr) = NullValue<int8_t>();
		break;
	case TypeId::SMALLINT:
		*((int16_t *)ptr) = NullValue<int16_t>();
		break;
	case TypeId::INTEGER:
		*((int32_t *)ptr) = NullValue<int32_t>();
		break;
	case TypeId::BIGINT:
		*((int64_t *)ptr) = NullValue<int64_t>();
		break;
	case TypeId::FLOAT:
		*((float *)ptr) = NullValue<float>();
		break;
	case TypeId::DOUBLE:
		*((double *)ptr) = NullValue<double>();
		break;
	case TypeId::VARCHAR:
		*((const char **)ptr) = NullValue<const char *>();
		break;
	default:
		throw InvalidTypeException(type, "Unsupported type for SetNullValue!");
	}
}

} // namespace duckdb
