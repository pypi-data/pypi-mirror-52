#include "execution/operator/order/physical_order.hpp"
#include "execution/physical_plan_generator.hpp"
#include "planner/operator/logical_order.hpp"

using namespace duckdb;
using namespace std;

unique_ptr<PhysicalOperator> PhysicalPlanGenerator::CreatePlan(LogicalOrder &op) {
	assert(op.children.size() == 1);

	auto plan = CreatePlan(*op.children[0]);

	auto order = make_unique<PhysicalOrder>(op, move(op.orders));
	order->children.push_back(move(plan));
	return move(order);
}
