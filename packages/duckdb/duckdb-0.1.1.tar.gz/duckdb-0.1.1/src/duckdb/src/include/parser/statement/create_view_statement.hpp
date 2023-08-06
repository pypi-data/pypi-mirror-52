//===----------------------------------------------------------------------===//
//                         DuckDB
//
// parser/statement/create_view_statement.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "parser/parsed_data/create_view_info.hpp"
#include "parser/sql_statement.hpp"

namespace duckdb {

class CreateViewStatement : public SQLStatement {
public:
	CreateViewStatement() : SQLStatement(StatementType::CREATE_VIEW), info(make_unique<CreateViewInfo>()){};

	unique_ptr<CreateViewInfo> info;
};

} // namespace duckdb
//
