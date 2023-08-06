//===----------------------------------------------------------------------===//
//                         DuckDB
//
// parser/statement/drop_statement.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "parser/parsed_data/drop_info.hpp"
#include "parser/sql_statement.hpp"

namespace duckdb {

class DropStatement : public SQLStatement {
public:
	DropStatement() : SQLStatement(StatementType::DROP), info(make_unique<DropInfo>()){};

	unique_ptr<DropInfo> info;
};

} // namespace duckdb
