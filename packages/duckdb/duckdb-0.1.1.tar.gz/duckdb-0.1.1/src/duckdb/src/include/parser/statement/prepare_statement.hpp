//===----------------------------------------------------------------------===//
//                         DuckDB
//
// parser/statement/prepare_statement.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "parser/parsed_expression.hpp"
#include "parser/sql_statement.hpp"

namespace duckdb {

class PrepareStatement : public SQLStatement {
public:
	PrepareStatement() : SQLStatement(StatementType::PREPARE), statement(nullptr), name("") {
	}

	unique_ptr<SQLStatement> statement;
	string name;
};
} // namespace duckdb
