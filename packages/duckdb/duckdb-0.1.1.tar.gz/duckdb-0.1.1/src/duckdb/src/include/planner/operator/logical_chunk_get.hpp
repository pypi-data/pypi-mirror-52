//===----------------------------------------------------------------------===//
//                         DuckDB
//
// planner/operator/logical_chunk_get.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/types/chunk_collection.hpp"
#include "planner/logical_operator.hpp"

namespace duckdb {

//! LogicalChunkGet represents a scan operation from a ChunkCollection
class LogicalChunkGet : public LogicalOperator {
public:
	LogicalChunkGet(index_t table_index, vector<TypeId> types, unique_ptr<ChunkCollection> collection)
	    : LogicalOperator(LogicalOperatorType::CHUNK_GET), table_index(table_index), collection(move(collection)) {
		assert(types.size() > 0);
		chunk_types = types;
	}

	//! The table index in the current bind context
	index_t table_index;
	//! The types of the chunk
	vector<TypeId> chunk_types;
	//! The chunk collection to scan
	unique_ptr<ChunkCollection> collection;

protected:
	void ResolveTypes() override {
		// types are resolved in the constructor
		this->types = chunk_types;
	}
};
} // namespace duckdb
