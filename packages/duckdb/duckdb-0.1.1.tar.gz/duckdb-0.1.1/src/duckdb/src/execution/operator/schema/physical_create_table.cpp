#include "execution/operator/schema/physical_create_table.hpp"

#include "catalog/catalog_entry/schema_catalog_entry.hpp"
#include "catalog/catalog_entry/table_catalog_entry.hpp"
#include "execution/expression_executor.hpp"
#include "main/client_context.hpp"
#include "storage/data_table.hpp"

using namespace duckdb;
using namespace std;

void PhysicalCreateTable::GetChunkInternal(ClientContext &context, DataChunk &chunk, PhysicalOperatorState *state) {
	int64_t inserted_count = 0;
	schema->CreateTable(context.ActiveTransaction(), info.get());
	if (children.size() > 0) {
		auto table = schema->GetTable(context.ActiveTransaction(), info->base->table);
		while (true) {
			children[0]->GetChunk(context, state->child_chunk, state->child_state.get());
			if (state->child_chunk.size() == 0) {
				break;
			}
			inserted_count += state->child_chunk.size();
			table->storage->Append(*table, context, state->child_chunk);
		}
	}

	chunk.data[0].count = 1;
	chunk.data[0].SetValue(0, Value::BIGINT(inserted_count));

	state->finished = true;
}
