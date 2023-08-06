//===----------------------------------------------------------------------===//
//                         DuckDB
//
// planner/parsed_data/bound_create_table_info.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "parser/parsed_data/create_table_info.hpp"
#include "planner/bound_constraint.hpp"
#include "planner/expression.hpp"
#include "storage/table/persistent_segment.hpp"

namespace duckdb {
class CatalogEntry;

struct BoundCreateTableInfo {
	BoundCreateTableInfo(unique_ptr<CreateTableInfo> base) : base(move(base)) {
	}
	//! The map of column names -> column index, used during binding
	unordered_map<string, column_t> name_map;
	//! List of constraints on the table
	vector<unique_ptr<Constraint>> constraints;
	//! List of bound constraints on the table
	vector<unique_ptr<BoundConstraint>> bound_constraints;
	//! Bound default values
	vector<unique_ptr<Expression>> bound_defaults;
	//! Dependents of the table (in e.g. default values)
	unordered_set<CatalogEntry *> dependencies;
	//! The existing table data on disk (if any)
	unique_ptr<vector<unique_ptr<PersistentSegment>>[]> data;
	//! The base create table info
	unique_ptr<CreateTableInfo> base;
};

} // namespace duckdb
