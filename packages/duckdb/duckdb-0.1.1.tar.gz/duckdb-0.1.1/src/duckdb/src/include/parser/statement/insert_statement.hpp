//===----------------------------------------------------------------------===//
//                         DuckDB
//
// parser/statement/insert_statement.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "parser/parsed_expression.hpp"
#include "parser/statement/select_statement.hpp"

#include <vector>

namespace duckdb {

class InsertStatement : public SQLStatement {
public:
	InsertStatement() : SQLStatement(StatementType::INSERT), schema(DEFAULT_SCHEMA){};

	//! The select statement to insert from
	unique_ptr<SelectStatement> select_statement;
	//! List of values to insert
	vector<vector<unique_ptr<ParsedExpression>>> values;
	//! Column names to insert into
	vector<string> columns;

	//! Table name to insert to
	string table;
	//! Schema name to insert to
	string schema;
};

} // namespace duckdb
