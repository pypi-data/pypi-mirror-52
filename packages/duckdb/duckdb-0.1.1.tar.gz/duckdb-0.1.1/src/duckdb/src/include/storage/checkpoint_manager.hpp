//===----------------------------------------------------------------------===//
//                         DuckDB
//
// storage/checkpoint_manager.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/common.hpp"
#include "common/types/chunk_collection.hpp"
#include "storage/storage_manager.hpp"
#include "storage/meta_block_writer.hpp"

namespace duckdb {
class ClientContext;
class MetaBlockReader;
class SchemaCatalogEntry;
class SequenceCatalogEntry;
class TableCatalogEntry;
class ViewCatalogEntry;

struct DataPointer {
	double min;
	double max;
	uint64_t row_start;
	uint64_t tuple_count;
	block_id_t block_id;
	uint32_t offset;
};

//! CheckpointManager is responsible for checkpointing the database
class CheckpointManager {
public:
	CheckpointManager(StorageManager &manager);

	//! Checkpoint the current state of the WAL and flush it to the main storage. This should be called BEFORE any
	//! connction is available because right now the checkpointing cannot be done online. (TODO)
	void CreateCheckpoint();
	//! Load from a stored checkpoint
	void LoadFromStorage();

	//! The block manager to write the checkpoint to
	BlockManager &block_manager;
	//! The database this storagemanager belongs to
	DuckDB &database;
	//! The metadata writer is responsible for writing schema information
	unique_ptr<MetaBlockWriter> metadata_writer;
	//! The table data writer is responsible for writing the DataPointers used by the table chunks
	unique_ptr<MetaBlockWriter> tabledata_writer;

private:
	void WriteSchema(Transaction &transaction, SchemaCatalogEntry &schema);
	void WriteTable(Transaction &transaction, TableCatalogEntry &table);
	void WriteView(Transaction &transaction, ViewCatalogEntry &table);
	void WriteSequence(Transaction &transaction, SequenceCatalogEntry &table);

	void ReadSchema(ClientContext &context, MetaBlockReader &reader);
	void ReadTable(ClientContext &context, MetaBlockReader &reader);
	void ReadView(ClientContext &context, MetaBlockReader &reader);
	void ReadSequence(ClientContext &context, MetaBlockReader &reader);
};

} // namespace duckdb
