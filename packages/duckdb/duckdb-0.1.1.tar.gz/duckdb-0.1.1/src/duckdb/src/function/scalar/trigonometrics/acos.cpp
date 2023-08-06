#include "function/scalar/trigonometric_functions.hpp"
#include "common/vector_operations/vector_operations.hpp"
#include "common/exception.hpp"

using namespace std;

namespace duckdb {

static void acos_function(ExpressionExecutor &exec, Vector inputs[], index_t input_count, BoundFunctionExpression &expr,
                   Vector &result) {
	assert(input_count == 1);
	inputs[0].Cast(TypeId::DOUBLE);
	result.Initialize(TypeId::DOUBLE);
	VectorOperations::ACos(inputs[0], result);
}

void Acos::RegisterFunction(BuiltinFunctions &set) {
	set.AddFunction(ScalarFunction("acos", { SQLType::DOUBLE }, SQLType::DOUBLE, acos_function));
}

}
