//===----------------------------------------------------------------------===//
//                         DuckDB
//
// planner/tableref/bound_basetableref.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "planner/bound_tableref.hpp"

namespace duckdb {
class TableCatalogEntry;

//! Represents a TableReference to a base table in the schema
class BoundBaseTableRef : public BoundTableRef {
public:
	BoundBaseTableRef(TableCatalogEntry *table, index_t bind_index)
	    : BoundTableRef(TableReferenceType::BASE_TABLE), table(table), bind_index(bind_index) {
	}

	//! The referenced table
	TableCatalogEntry *table;
	//! The set of columns bound to this base table reference
	vector<string> bound_columns;
	//! The index in the bind context
	index_t bind_index;
};
} // namespace duckdb
