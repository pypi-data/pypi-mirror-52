#include "execution/operator/schema/physical_create_index.hpp"

#include "catalog/catalog_entry/schema_catalog_entry.hpp"
#include "catalog/catalog_entry/table_catalog_entry.hpp"
#include "execution/expression_executor.hpp"
#include "main/client_context.hpp"

using namespace duckdb;
using namespace std;

void PhysicalCreateIndex::CreateARTIndex() {
	auto art = make_unique<ART>(*table.storage, column_ids, move(unbound_expressions));

	table.storage->AddIndex(move(art), expressions);
}

void PhysicalCreateIndex::GetChunkInternal(ClientContext &context, DataChunk &chunk, PhysicalOperatorState *state) {
	if (column_ids.size() == 0) {
		throw NotImplementedException("CREATE INDEX does not refer to any columns in the base table!");
	}

	auto &schema = *table.schema;
	if (!schema.CreateIndex(context.ActiveTransaction(), info.get())) {
		// index already exists, but error ignored because of CREATE ... IF NOT
		// EXISTS
		return;
	}

	// create the chunk to hold intermediate expression results
	// "Multidimensional indexes not supported yet"
	assert(expressions.size() == 1);

	switch (info->index_type) {
	case IndexType::ART: {
		CreateARTIndex();
		break;
	}
	default:
		assert(0);
		throw NotImplementedException("Unimplemented index type");
	}

	chunk.data[0].count = 0;

	state->finished = true;
}
