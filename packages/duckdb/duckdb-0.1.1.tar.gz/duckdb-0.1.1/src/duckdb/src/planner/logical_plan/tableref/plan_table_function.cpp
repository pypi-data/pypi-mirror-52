#include "planner/logical_plan_generator.hpp"
#include "planner/operator/logical_table_function.hpp"
#include "planner/tableref/bound_table_function.hpp"

using namespace duckdb;
using namespace std;

unique_ptr<LogicalOperator> LogicalPlanGenerator::CreatePlan(BoundTableFunction &ref) {
	return make_unique<LogicalTableFunction>(ref.function, ref.bind_index, move(ref.parameters));
}
