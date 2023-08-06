#include "function/scalar/trigonometric_functions.hpp"
#include "common/vector_operations/vector_operations.hpp"
#include "common/exception.hpp"

using namespace std;

namespace duckdb {

static void tan_function(ExpressionExecutor &exec, Vector inputs[], index_t input_count, BoundFunctionExpression &expr,
                  Vector &result) {
	assert(input_count == 1);
	inputs[0].Cast(TypeId::DOUBLE);
	result.Initialize(TypeId::DOUBLE);
	VectorOperations::Tan(inputs[0], result);
}

void Tan::RegisterFunction(BuiltinFunctions &set) {
	set.AddFunction(ScalarFunction("tan", { SQLType::DOUBLE }, SQLType::DOUBLE, tan_function));
}

}
