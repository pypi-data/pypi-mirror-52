#include "common/types/hash.hpp"

#include "common/exception.hpp"
#include "common/operator/numeric_functions.hpp"
#include "common/value_operations/value_operations.hpp"

using namespace duckdb;
using namespace std;

uint64_t ValueOperations::Hash(const Value &op) {
	if (op.is_null) {
		return 0;
	}
	switch (op.type) {
	case TypeId::BOOLEAN:
		return duckdb::Hash(op.value_.boolean);
	case TypeId::TINYINT:
		return duckdb::Hash(op.value_.tinyint);
	case TypeId::SMALLINT:
		return duckdb::Hash(op.value_.smallint);
	case TypeId::INTEGER:
		return duckdb::Hash(op.value_.integer);
	case TypeId::BIGINT:
		return duckdb::Hash(op.value_.bigint);
	case TypeId::FLOAT:
		return duckdb::Hash(op.value_.float_);
	case TypeId::DOUBLE:
		return duckdb::Hash(op.value_.double_);
	case TypeId::POINTER:
		return duckdb::Hash(op.value_.pointer);
	case TypeId::VARCHAR:
		return duckdb::Hash(op.str_value.c_str());
	default:
		throw NotImplementedException("Unimplemented type for hash");
	}
}
