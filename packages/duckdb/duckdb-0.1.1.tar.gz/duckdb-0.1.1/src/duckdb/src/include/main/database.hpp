//===----------------------------------------------------------------------===//
//                         DuckDB
//
// main/database.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/common.hpp"
#include "common/file_system.hpp"

namespace duckdb {
class StorageManager;
class Catalog;
class TransactionManager;
class ConnectionManager;
class FileSystem;

enum AccessMode { UNDEFINED, READ_ONLY, READ_WRITE }; // TODO AUTOMATIC

// this is optional and only used in tests at the moment
struct DBConfig {
	friend class DuckDB;
	friend class StorageManager;

public:
	~DBConfig();

	//! Access mode of the database (READ_ONLY or READ_WRITE)
	AccessMode access_mode = AccessMode::UNDEFINED;
	// Checkpoint when WAL reaches this size
	index_t checkpoint_wal_size = 1 << 20;
	//! Whether or not to use Direct IO, bypassing operating system buffers
	bool use_direct_io = false;
	//! The FileSystem to use, can be overwritten to allow for injecting custom file systems for testing purposes (e.g.
	//! RamFS or something similar)
	unique_ptr<FileSystem> file_system;

private:
	// FIXME: don't set this as a user: used internally (only for now)
	bool checkpoint_only = false;
};

//! The database object. This object holds the catalog and all the
//! database-specific meta information.
class Connection;
class DuckDB {
public:
	DuckDB(const char *path = nullptr, DBConfig *config = nullptr);
	DuckDB(const string &path, DBConfig *config = nullptr);

	~DuckDB();

	unique_ptr<FileSystem> file_system;
	unique_ptr<StorageManager> storage;
	unique_ptr<Catalog> catalog;
	unique_ptr<TransactionManager> transaction_manager;
	unique_ptr<ConnectionManager> connection_manager;

	AccessMode access_mode;
	bool use_direct_io;
	bool checkpoint_only;
	index_t checkpoint_wal_size;

private:
	void Configure(DBConfig &config);
};

} // namespace duckdb
