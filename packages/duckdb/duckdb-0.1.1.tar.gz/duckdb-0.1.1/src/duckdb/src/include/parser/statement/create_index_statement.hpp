//===----------------------------------------------------------------------===//
//                         DuckDB
//
// parser/statement/create_index_statement.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "parser/column_definition.hpp"
#include "parser/parsed_data/create_index_info.hpp"
#include "parser/sql_statement.hpp"
#include "parser/tableref/basetableref.hpp"

namespace duckdb {

class CreateIndexStatement : public SQLStatement {
public:
	CreateIndexStatement() : SQLStatement(StatementType::CREATE_INDEX), info(make_unique<CreateIndexInfo>()){};

	//! The table to create the index on
	unique_ptr<BaseTableRef> table;
	//! Set of expressions to index by
	vector<unique_ptr<ParsedExpression>> expressions;
	// Info for index creation
	unique_ptr<CreateIndexInfo> info;
};

} // namespace duckdb
//
