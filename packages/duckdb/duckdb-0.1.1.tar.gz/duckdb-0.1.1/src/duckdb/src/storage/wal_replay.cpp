#include "storage/write_ahead_log.hpp"
#include "common/serializer/buffered_file_reader.hpp"

#include "parser/parsed_data/drop_info.hpp"

using namespace duckdb;
using namespace std;

class ReplayState {
public:
	ReplayState(DuckDB &db, ClientContext &context, Deserializer &source)
	    : db(db), context(context), source(source), current_table(nullptr) {
	}

	DuckDB &db;
	ClientContext &context;
	Deserializer &source;
	TableCatalogEntry *current_table;

public:
	void ReplayEntry(WALType entry_type);

private:
	void ReplayCreateTable();
	void ReplayDropTable();

	void ReplayCreateView();
	void ReplayDropView();

	void ReplayCreateSchema();
	void ReplayDropSchema();

	void ReplayCreateSequence();
	void ReplayDropSequence();
	void ReplaySequenceValue();

	void ReplayUseTable();
	void ReplayInsert();
	void ReplayDelete();
	void ReplayUpdate();

	void ReplayQuery();
};

void WriteAheadLog::Replay(DuckDB &database, string &path) {
	BufferedFileReader reader(*database.file_system, path.c_str());

	if (reader.Finished()) {
		// WAL is empty
		return;
	}

	ClientContext context(database);
	context.transaction.SetAutoCommit(false);
	context.transaction.BeginTransaction();

	ReplayState state(database, context, reader);

	// replay the WAL
	// note that everything is wrapped inside a try/catch block here
	// there can be errors in WAL replay because of a corrupt WAL file
	// in this case we should throw a warning but startup anyway
	try {
		while (true) {
			// read the current entry
			WALType entry_type = reader.Read<WALType>();
			if (entry_type == WALType::WAL_FLUSH) {
				// flush: commit the current transaction
				context.transaction.Commit();
				// check if the file is exhausted
				if (reader.Finished()) {
					// we finished reading the file: break
					break;
				}
				// otherwise we keep on reading
				context.transaction.BeginTransaction();
			} else {
				// replay the entry
				state.ReplayEntry(entry_type);
			}
		}
	} catch (std::exception &ex) {
		// FIXME: this report a proper warning in the connection
		fprintf(stderr, "Exception in WAL playback: %s\n", ex.what());
		// exception thrown in WAL replay: rollback
		context.transaction.Rollback();
	}
}

//===--------------------------------------------------------------------===//
// Replay Entries
//===--------------------------------------------------------------------===//
void ReplayState::ReplayEntry(WALType entry_type) {
	switch (entry_type) {
	case WALType::CREATE_TABLE:
		ReplayCreateTable();
		break;
	case WALType::DROP_TABLE:
		ReplayDropTable();
		break;
	case WALType::CREATE_VIEW:
		ReplayCreateView();
		break;
	case WALType::DROP_VIEW:
		ReplayDropView();
		break;
	case WALType::CREATE_SCHEMA:
		ReplayCreateSchema();
		break;
	case WALType::DROP_SCHEMA:
		ReplayDropSchema();
		break;
	case WALType::CREATE_SEQUENCE:
		ReplayCreateSequence();
		break;
	case WALType::DROP_SEQUENCE:
		ReplayDropSequence();
		break;
	case WALType::SEQUENCE_VALUE:
		ReplaySequenceValue();
		break;
	case WALType::USE_TABLE:
		ReplayUseTable();
		break;
	case WALType::INSERT_TUPLE:
		ReplayInsert();
		break;
	case WALType::DELETE_TUPLE:
		ReplayDelete();
		break;
	case WALType::UPDATE_TUPLE:
		ReplayUpdate();
		break;
	case WALType::QUERY:
		ReplayQuery();
		break;
	default:
		throw Exception("Invalid WAL entry type!");
	}
}

//===--------------------------------------------------------------------===//
// Replay Table
//===--------------------------------------------------------------------===//
void ReplayState::ReplayCreateTable() {
	auto info = TableCatalogEntry::Deserialize(source);

	// bind the constraints to the table again
	Binder binder(context);
	auto bound_info = binder.BindCreateTableInfo(move(info));

	db.catalog->CreateTable(context.ActiveTransaction(), bound_info.get());
}

void ReplayState::ReplayDropTable() {
	DropInfo info;

	info.type = CatalogType::TABLE;
	info.schema = source.Read<string>();
	info.name = source.Read<string>();

	db.catalog->DropTable(context.ActiveTransaction(), &info);
}

//===--------------------------------------------------------------------===//
// Replay View
//===--------------------------------------------------------------------===//
void ReplayState::ReplayCreateView() {
	auto entry = ViewCatalogEntry::Deserialize(source);

	db.catalog->CreateView(context.ActiveTransaction(), entry.get());
}

void ReplayState::ReplayDropView() {
	DropInfo info;
	info.type = CatalogType::VIEW;
	info.schema = source.Read<string>();
	info.name = source.Read<string>();
	db.catalog->DropView(context.ActiveTransaction(), &info);
}

//===--------------------------------------------------------------------===//
// Replay Schema
//===--------------------------------------------------------------------===//
void ReplayState::ReplayCreateSchema() {
	CreateSchemaInfo info;
	info.schema = source.Read<string>();

	db.catalog->CreateSchema(context.ActiveTransaction(), &info);
}

void ReplayState::ReplayDropSchema() {
	DropInfo info;

	info.type = CatalogType::SCHEMA;
	info.name = source.Read<string>();

	db.catalog->DropSchema(context.ActiveTransaction(), &info);
}

//===--------------------------------------------------------------------===//
// Replay Sequence
//===--------------------------------------------------------------------===//
void ReplayState::ReplayCreateSequence() {
	auto entry = SequenceCatalogEntry::Deserialize(source);

	db.catalog->CreateSequence(context.ActiveTransaction(), entry.get());
}

void ReplayState::ReplayDropSequence() {
	DropInfo info;
	info.type = CatalogType::SEQUENCE;
	info.schema = source.Read<string>();
	info.name = source.Read<string>();

	db.catalog->DropSequence(context.ActiveTransaction(), &info);
}

void ReplayState::ReplaySequenceValue() {
	auto schema = source.Read<string>();
	auto name = source.Read<string>();
	auto usage_count = source.Read<uint64_t>();
	auto counter = source.Read<int64_t>();

	// fetch the sequence from the catalog
	auto seq = db.catalog->GetSequence(context.ActiveTransaction(), schema, name);
	if (usage_count > seq->usage_count) {
		seq->usage_count = usage_count;
		seq->counter = counter;
	}
}

//===--------------------------------------------------------------------===//
// Replay Data
//===--------------------------------------------------------------------===//
void ReplayState::ReplayUseTable() {
	auto schema_name = source.Read<string>();
	auto table_name = source.Read<string>();
	current_table = db.catalog->GetTable(context.ActiveTransaction(), schema_name, table_name);
}

void ReplayState::ReplayInsert() {
	if (!current_table) {
		throw Exception("Corrupt WAL: insert without table");
	}
	DataChunk chunk;
	chunk.Deserialize(source);

	// append to the current table
	current_table->storage->Append(*current_table, context, chunk);
}

void ReplayState::ReplayDelete() {
	if (!current_table) {
		throw Exception("Corrupt WAL: delete without table");
	}
	DataChunk chunk;
	chunk.Deserialize(source);

	assert(chunk.column_count == 1 && chunk.data[0].type == ROW_TYPE);
	row_t row_ids[1];
	Vector row_identifiers(ROW_TYPE, (data_ptr_t)row_ids);
	row_identifiers.count = 1;

	auto source_ids = (row_t *)chunk.data[0].data;
	// delete the tuples from the current table
	for (index_t i = 0; i < chunk.size(); i++) {
		row_ids[0] = source_ids[i];
		current_table->storage->Delete(*current_table, context, row_identifiers);
	}
}

void ReplayState::ReplayUpdate() {
	if (!current_table) {
		throw Exception("Corrupt WAL: update without table");
	}
	DataChunk chunk;
	chunk.Deserialize(source);

	vector<column_t> column_ids;
	for (index_t i = 0; i < chunk.column_count - 1; i++) {
		column_ids.push_back(i);
	}

	index_t update_count = chunk.size();
	for (index_t i = 0; i < chunk.column_count; i++) {
		chunk.data[i].sel_vector = chunk.owned_sel_vector;
		chunk.data[i].count = 1;
	}
	chunk.sel_vector = chunk.owned_sel_vector;
	chunk.column_count = chunk.column_count - 1;

	auto &row_ids = chunk.data[chunk.column_count];

	for (index_t i = 0; i < update_count; i++) {
		chunk.owned_sel_vector[0] = i;
		current_table->storage->Update(*current_table, context, row_ids, column_ids, chunk);
	}
}

//===--------------------------------------------------------------------===//
// Query
//===--------------------------------------------------------------------===//
void ReplayState::ReplayQuery() {
	// read the query
	auto query = source.Read<string>();

	context.Query(query, false);
}
