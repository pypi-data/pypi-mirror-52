#include "storage/checkpoint_manager.hpp"
#include "storage/block_manager.hpp"
#include "storage/meta_block_reader.hpp"

#include "common/serializer.hpp"
#include "common/vector_operations/vector_operations.hpp"
#include "common/types/null_value.hpp"

#include "catalog/catalog.hpp"
#include "catalog/catalog_entry/schema_catalog_entry.hpp"
#include "catalog/catalog_entry/sequence_catalog_entry.hpp"
#include "catalog/catalog_entry/table_catalog_entry.hpp"
#include "catalog/catalog_entry/view_catalog_entry.hpp"

#include "parser/parsed_data/create_schema_info.hpp"
#include "parser/parsed_data/create_table_info.hpp"
#include "parser/parsed_data/create_view_info.hpp"

#include "planner/binder.hpp"
#include "planner/parsed_data/bound_create_table_info.hpp"

#include "main/client_context.hpp"
#include "main/database.hpp"

#include "transaction/transaction_manager.hpp"

#include "storage/checkpoint/table_data_writer.hpp"
#include "storage/checkpoint/table_data_reader.hpp"

using namespace duckdb;
using namespace std;

// constexpr uint64_t CheckpointManager::DATA_BLOCK_HEADER_SIZE;

CheckpointManager::CheckpointManager(StorageManager &manager)
    : block_manager(*manager.block_manager), database(manager.database) {
}

void CheckpointManager::CreateCheckpoint() {
	// assert that the checkpoint manager hasn't been used before
	assert(!metadata_writer);

	auto transaction = database.transaction_manager->StartTransaction();

	//! Set up the writers for the checkpoints
	metadata_writer = make_unique<MetaBlockWriter>(block_manager);
	tabledata_writer = make_unique<MetaBlockWriter>(block_manager);

	// get the id of the first meta block
	block_id_t meta_block = metadata_writer->block->id;

	vector<SchemaCatalogEntry *> schemas;
	// we scan the schemas
	database.catalog->schemas.Scan(*transaction,
	                               [&](CatalogEntry *entry) { schemas.push_back((SchemaCatalogEntry *)entry); });
	// write the actual data into the database
	// write the amount of schemas
	metadata_writer->Write<uint32_t>(schemas.size());
	for (auto &schema : schemas) {
		WriteSchema(*transaction, *schema);
	}
	// flush the meta data to disk
	metadata_writer->Flush();
	tabledata_writer->Flush();

	// finally write the updated header
	DatabaseHeader header;
	header.meta_block = meta_block;
	block_manager.WriteHeader(header);
}

void CheckpointManager::LoadFromStorage() {
	block_id_t meta_block = block_manager.GetMetaBlock();
	if (meta_block < 0) {
		// storage is empty
		return;
	}

	ClientContext context(database);
	context.transaction.BeginTransaction();
	// create the MetaBlockReader to read from the storage
	MetaBlockReader reader(block_manager, meta_block);
	uint32_t schema_count = reader.Read<uint32_t>();
	for (uint32_t i = 0; i < schema_count; i++) {
		ReadSchema(context, reader);
	}
	context.transaction.Commit();
}

//===--------------------------------------------------------------------===//
// Schema
//===--------------------------------------------------------------------===//
void CheckpointManager::WriteSchema(Transaction &transaction, SchemaCatalogEntry &schema) {
	// write the schema data
	schema.Serialize(*metadata_writer);
	// then, we fetch the tables/views/sequences information
	vector<TableCatalogEntry *> tables;
	vector<ViewCatalogEntry *> views;
	schema.tables.Scan(transaction, [&](CatalogEntry *entry) {
		if (entry->type == CatalogType::TABLE) {
			tables.push_back((TableCatalogEntry *)entry);
		} else if (entry->type == CatalogType::VIEW) {
			views.push_back((ViewCatalogEntry *)entry);
		} else {
			throw NotImplementedException("Catalog type for entries");
		}
	});
	vector<SequenceCatalogEntry *> sequences;
	schema.sequences.Scan(transaction,
	                      [&](CatalogEntry *entry) { sequences.push_back((SequenceCatalogEntry *)entry); });

	// write the sequences
	metadata_writer->Write<uint32_t>(sequences.size());
	for (auto &seq : sequences) {
		WriteSequence(transaction, *seq);
	}
	// now write the tables
	metadata_writer->Write<uint32_t>(tables.size());
	for (auto &table : tables) {
		WriteTable(transaction, *table);
	}
	// finally write the views
	metadata_writer->Write<uint32_t>(views.size());
	for (auto &view : views) {
		WriteView(transaction, *view);
	}
	// FIXME: free list?
}

void CheckpointManager::ReadSchema(ClientContext &context, MetaBlockReader &reader) {
	// read the schema and create it in the catalog
	auto info = SchemaCatalogEntry::Deserialize(reader);
	// we set if_not_exists to true to ignore the failure of recreating the main schema
	info->if_not_exists = true;
	database.catalog->CreateSchema(context.ActiveTransaction(), info.get());

	// read the sequences
	uint32_t seq_count = reader.Read<uint32_t>();
	for (uint32_t i = 0; i < seq_count; i++) {
		ReadSequence(context, reader);
	}
	// read the table count and recreate the tables
	uint32_t table_count = reader.Read<uint32_t>();
	for (uint32_t i = 0; i < table_count; i++) {
		ReadTable(context, reader);
	}
	// finally read the views
	uint32_t view_count = reader.Read<uint32_t>();
	for (uint32_t i = 0; i < view_count; i++) {
		ReadView(context, reader);
	}
}

//===--------------------------------------------------------------------===//
// Views
//===--------------------------------------------------------------------===//
void CheckpointManager::WriteView(Transaction &transaction, ViewCatalogEntry &view) {
	view.Serialize(*metadata_writer);
}

void CheckpointManager::ReadView(ClientContext &context, MetaBlockReader &reader) {
	auto info = ViewCatalogEntry::Deserialize(reader);

	database.catalog->CreateView(context.ActiveTransaction(), info.get());
}

//===--------------------------------------------------------------------===//
// Sequences
//===--------------------------------------------------------------------===//
void CheckpointManager::WriteSequence(Transaction &transaction, SequenceCatalogEntry &seq) {
	seq.Serialize(*metadata_writer);
}

void CheckpointManager::ReadSequence(ClientContext &context, MetaBlockReader &reader) {
	auto info = SequenceCatalogEntry::Deserialize(reader);

	database.catalog->CreateSequence(context.ActiveTransaction(), info.get());
}

//===--------------------------------------------------------------------===//
// Table Metadata
//===--------------------------------------------------------------------===//
void CheckpointManager::WriteTable(Transaction &transaction, TableCatalogEntry &table) {
	// write the table meta data
	table.Serialize(*metadata_writer);
	//! write the blockId for the table info
	metadata_writer->Write<block_id_t>(tabledata_writer->block->id);
	//! and the offset to where the info starts
	metadata_writer->Write<uint64_t>(tabledata_writer->offset);
	// now we need to write the table data
	TableDataWriter writer(*this, table);
	writer.WriteTableData(transaction);
}

void CheckpointManager::ReadTable(ClientContext &context, MetaBlockReader &reader) {
	// deserialize the table meta data
	auto info = TableCatalogEntry::Deserialize(reader);
	// bind the info
	Binder binder(context);
	auto bound_info = binder.BindCreateTableInfo(move(info));

	// now read the actual table data and place it into the create table info
	auto block_id = reader.Read<block_id_t>();
	auto offset = reader.Read<uint64_t>();
	MetaBlockReader table_data_reader(block_manager, block_id);
	table_data_reader.offset = offset;
	TableDataReader data_reader(*this, table_data_reader, *bound_info);
	data_reader.ReadTableData();

	// finally create the table in the catalog
	database.catalog->CreateTable(context.ActiveTransaction(), bound_info.get());
}
