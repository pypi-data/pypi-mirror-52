//===----------------------------------------------------------------------===//
//                         DuckDB
//
// parser/statement/execute_statement.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "parser/parsed_expression.hpp"
#include "parser/sql_statement.hpp"

namespace duckdb {

class ExecuteStatement : public SQLStatement {
public:
	ExecuteStatement() : SQLStatement(StatementType::EXECUTE){};

	string name;
	vector<unique_ptr<ParsedExpression>> values;
};
} // namespace duckdb
