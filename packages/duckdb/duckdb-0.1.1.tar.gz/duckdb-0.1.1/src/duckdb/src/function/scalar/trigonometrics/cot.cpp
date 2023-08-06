#include "function/scalar/trigonometric_functions.hpp"
#include "common/vector_operations/vector_operations.hpp"
#include "common/types/constant_vector.hpp"
#include "common/types/static_vector.hpp"
#include "common/exception.hpp"

using namespace std;

namespace duckdb {

static void cot_function(ExpressionExecutor &exec, Vector inputs[], index_t input_count, BoundFunctionExpression &expr,
                  Vector &result) {
	assert(input_count == 1);
	inputs[0].Cast(TypeId::DOUBLE);
	result.Initialize(TypeId::DOUBLE);
	ConstantVector one(Value((double)1.0));
	StaticVector<double> tan_res;
	VectorOperations::Tan(inputs[0], tan_res);
	VectorOperations::Divide(one, tan_res, result);
}

void Cot::RegisterFunction(BuiltinFunctions &set) {
	set.AddFunction(ScalarFunction("cot", { SQLType::DOUBLE }, SQLType::DOUBLE, cot_function));
}

}
