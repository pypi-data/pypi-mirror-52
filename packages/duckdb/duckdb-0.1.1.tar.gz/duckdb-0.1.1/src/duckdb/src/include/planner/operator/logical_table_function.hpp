//===----------------------------------------------------------------------===//
//                         DuckDB
//
// planner/operator/logical_table_function.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "planner/logical_operator.hpp"

namespace duckdb {

//! LogicalTableFunction represents a call to a table-producing function
class LogicalTableFunction : public LogicalOperator {
public:
	LogicalTableFunction(TableFunctionCatalogEntry *function, index_t table_index,
	                     vector<unique_ptr<Expression>> parameters)
	    : LogicalOperator(LogicalOperatorType::TABLE_FUNCTION), function(function), table_index(table_index) {
		expressions = move(parameters);
	}

	//! The function
	TableFunctionCatalogEntry *function;
	//! The table index of the table-producing function
	index_t table_index;

protected:
	void ResolveTypes() override;
};
} // namespace duckdb
