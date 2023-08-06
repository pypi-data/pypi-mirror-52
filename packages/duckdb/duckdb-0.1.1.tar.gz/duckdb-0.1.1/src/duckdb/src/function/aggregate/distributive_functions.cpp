#include "function/aggregate/distributive_functions.hpp"
#include "common/exception.hpp"
#include "common/types/null_value.hpp"
#include "common/vector_operations/vector_operations.hpp"
#include "function/aggregate_function.hpp"

using namespace std;

namespace duckdb {

void gather_finalize(Vector &states, Vector &result) {
	VectorOperations::Gather::Set(states, result);
}

void null_state_initialize(data_ptr_t state, TypeId return_type) {
	SetNullValue(state, return_type);
}

index_t get_bigint_type_size(TypeId return_type) {
	return GetTypeIdSize(TypeId::BIGINT);
}

void bigint_payload_initialize(data_ptr_t payload, TypeId return_type) {
	memset(payload, 0, get_bigint_type_size(return_type));
}

Value bigint_simple_initialize() {
	return Value::BIGINT(0);
}
index_t get_return_type_size(TypeId return_type) {
	return GetTypeIdSize(return_type);
}

Value null_simple_initialize() {
	return Value();
}

void BuiltinFunctions::RegisterDistributiveAggregates() {
	Register<CountStar>();
	Register<Count>();
	Register<First>();
	Register<Max>();
	Register<Min>();
	Register<Sum>();
	Register<StringAgg>();
}

} // namespace duckdb

