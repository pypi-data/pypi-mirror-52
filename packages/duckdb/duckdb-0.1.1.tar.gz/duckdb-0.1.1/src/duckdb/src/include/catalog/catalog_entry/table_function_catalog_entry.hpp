//===----------------------------------------------------------------------===//
//                         DuckDB
//
// catalog/catalog_entry/table_function_catalog_entry.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "catalog/catalog_entry.hpp"
#include "common/unordered_map.hpp"
#include "function/table_function.hpp"

namespace duckdb {

class Catalog;
class Constraint;
class SchemaCatalogEntry;

struct CreateTableFunctionInfo;

//! A table function in the catalog
class TableFunctionCatalogEntry : public CatalogEntry {
public:
	TableFunctionCatalogEntry(Catalog *catalog, SchemaCatalogEntry *schema, CreateTableFunctionInfo *info);

	//! The schema the table belongs to
	SchemaCatalogEntry *schema;
	//! The table function
	TableFunction function;
	//! A map of return-column name to column index
	unordered_map<string, column_t> name_map;

	//! Returns whether or not a column with the given name is returned by the
	//! function
	bool ColumnExists(const string &name);
	//! Returns a list of return-types of the function
	vector<TypeId> GetTypes();
};
} // namespace duckdb
