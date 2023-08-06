//===----------------------------------------------------------------------===//
//                         DuckDB
//
// catalog/catalog_entry.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/common.hpp"
#include "common/enums/catalog_type.hpp"
#include "common/exception.hpp"

namespace duckdb {
struct AlterInfo;
class Catalog;
class CatalogSet;
class ClientContext;
class Transaction;

//! Abstract base class of an entry in the catalog
class CatalogEntry {
public:
	CatalogEntry(CatalogType type, Catalog *catalog, string name)
	    : type(type), catalog(catalog), set(nullptr), name(name), deleted(false), parent(nullptr) {
	}

	virtual ~CatalogEntry();

	virtual unique_ptr<CatalogEntry> AlterEntry(ClientContext &context, AlterInfo *info) {
		throw CatalogException("Unsupported alter type for catalog entry!");
	}

	//! The type of this catalog entry
	CatalogType type;
	//! Reference to the catalog this entry belongs to
	Catalog *catalog;
	//! Reference to the catalog set this entry is stored in
	CatalogSet *set;
	//! The name of the entry
	string name;
	//! Whether or not the object is deleted
	bool deleted;
	//! Timestamp at which the catalog entry was created
	transaction_t timestamp;
	//! Child entry
	unique_ptr<CatalogEntry> child;
	//! Parent entry (the node that owns this node)
	CatalogEntry *parent;
};
} // namespace duckdb
