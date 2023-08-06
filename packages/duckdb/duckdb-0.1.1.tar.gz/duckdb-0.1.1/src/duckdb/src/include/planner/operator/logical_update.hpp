//===----------------------------------------------------------------------===//
//                         DuckDB
//
// planner/operator/logical_update.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "planner/logical_operator.hpp"

namespace duckdb {

class LogicalUpdate : public LogicalOperator {
public:
	LogicalUpdate(TableCatalogEntry *table, vector<column_t> columns, vector<unique_ptr<Expression>> expressions,
	              vector<unique_ptr<Expression>> bound_defaults)
	    : LogicalOperator(LogicalOperatorType::UPDATE, std::move(expressions)), table(table), columns(columns),
	      bound_defaults(move(bound_defaults)) {
	}

	TableCatalogEntry *table;
	vector<column_t> columns;
	vector<unique_ptr<Expression>> bound_defaults;

protected:
	void ResolveTypes() override {
		types.push_back(TypeId::BIGINT);
	}
};
} // namespace duckdb
