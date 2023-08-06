#include "execution/operator/helper/physical_prune_columns.hpp"

#include "execution/expression_executor.hpp"

using namespace duckdb;
using namespace std;

void PhysicalPruneColumns::GetChunkInternal(ClientContext &context, DataChunk &chunk, PhysicalOperatorState *state_) {
	auto state = reinterpret_cast<PhysicalOperatorState *>(state_);

	children[0]->GetChunk(context, state->child_chunk, state->child_state.get());
	if (state->child_chunk.size() == 0) {
		return;
	}
	assert(column_limit <= state->child_chunk.column_count);
	for (index_t i = 0; i < column_limit; i++) {
		chunk.data[i].Reference(state->child_chunk.data[i]);
	}
	chunk.sel_vector = state->child_chunk.sel_vector;
}
