#include "execution/operator/aggregate/physical_simple_aggregate.hpp"

#include "common/vector_operations/vector_operations.hpp"
#include "execution/expression_executor.hpp"
#include "planner/expression/bound_aggregate_expression.hpp"
#include "catalog/catalog_entry/aggregate_function_catalog_entry.hpp"

using namespace duckdb;
using namespace std;

PhysicalSimpleAggregate::PhysicalSimpleAggregate(vector<TypeId> types, vector<unique_ptr<Expression>> expressions)
    : PhysicalOperator(PhysicalOperatorType::SIMPLE_AGGREGATE, types), aggregates(move(expressions)) {
}

void PhysicalSimpleAggregate::GetChunkInternal(ClientContext &context, DataChunk &chunk,
                                               PhysicalOperatorState *state_) {
	auto state = reinterpret_cast<PhysicalSimpleAggregateOperatorState *>(state_);
	while (true) {
		// iterate over the child
		children[0]->GetChunk(context, state->child_chunk, state->child_state.get());
		if (state->child_chunk.size() == 0) {
			break;
		}
		ExpressionExecutor executor(state->child_chunk);
		// now resolve the aggregates for each of the children
		index_t payload_idx = 0;
		DataChunk &payload_chunk = state->payload_chunk;
		payload_chunk.Reset();
		for (index_t aggr_idx = 0; aggr_idx < aggregates.size(); aggr_idx++) {
			auto &aggregate = (BoundAggregateExpression &)*aggregates[aggr_idx];
			index_t payload_cnt = 0;
			// resolve the child expression of the aggregate (if any)
			if (aggregate.children.size()) {
				for (index_t i = 0; i < aggregate.children.size(); ++i) {
					executor.ExecuteExpression(*aggregate.children[i], payload_chunk.data[payload_idx + payload_cnt]);
					++payload_cnt;
				}
			} else {
				payload_chunk.data[payload_idx + payload_cnt].count = state->child_chunk.size();
				++payload_cnt;
			}
			// perform the actual aggregation
			assert(aggregate.function.simple_update);
			aggregate.function.simple_update(&payload_chunk.data[payload_idx], payload_cnt, state->aggregates[aggr_idx]);

			payload_idx += payload_cnt;
		}
	}
	// initialize the result chunk with the aggregate values
	for (index_t aggr_idx = 0; aggr_idx < aggregates.size(); aggr_idx++) {
		chunk.data[aggr_idx].count = 1;
		chunk.data[aggr_idx].SetValue(0, state->aggregates[aggr_idx]);
	}
	state->finished = true;
}

unique_ptr<PhysicalOperatorState> PhysicalSimpleAggregate::GetOperatorState() {
	return make_unique<PhysicalSimpleAggregateOperatorState>(this, children[0].get());
}

PhysicalSimpleAggregateOperatorState::PhysicalSimpleAggregateOperatorState(PhysicalSimpleAggregate *parent,
                                                                           PhysicalOperator *child)
    : PhysicalOperatorState(child) {
	vector<TypeId> payload_types;
	for (auto &aggregate : parent->aggregates) {
		assert(aggregate->GetExpressionClass() == ExpressionClass::BOUND_AGGREGATE);
		auto &aggr = (BoundAggregateExpression &)*aggregate;
		// initialize the payload chunk
		if (aggr.children.size()) {
			for (index_t i = 0; i < aggr.children.size(); ++i) {
				payload_types.push_back(aggr.children[i]->return_type);
			}
		} else {
			// COUNT(*)
			payload_types.push_back(TypeId::BIGINT);
		}
		// initialize the aggregate values
		assert(aggr.function.simple_initialize);
		aggregates.push_back(aggr.function.simple_initialize());
	}
	payload_chunk.Initialize(payload_types);
}
