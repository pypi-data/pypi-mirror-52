//===----------------------------------------------------------------------===//
//                         DuckDB
//
// planner/bound_sql_statement.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/common.hpp"
#include "common/enums/statement_type.hpp"

namespace duckdb {
//! Bound equivalent of SQLStatement
class BoundSQLStatement {
public:
	BoundSQLStatement(StatementType type) : type(type){};
	virtual ~BoundSQLStatement() {
	}

	virtual vector<string> GetNames() = 0;
	virtual vector<SQLType> GetTypes() = 0;

	StatementType type;
};
} // namespace duckdb
