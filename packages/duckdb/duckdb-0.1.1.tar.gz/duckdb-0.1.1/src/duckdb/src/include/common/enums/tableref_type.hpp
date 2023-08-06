//===----------------------------------------------------------------------===//
//                         DuckDB
//
// common/enums/tableref_type.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/constants.hpp"

namespace duckdb {

//===--------------------------------------------------------------------===//
// Table Reference Types
//===--------------------------------------------------------------------===//
enum class TableReferenceType : uint8_t {
	INVALID = 0,       // invalid table reference type
	BASE_TABLE = 1,    // base table reference
	SUBQUERY = 2,      // output of a subquery
	JOIN = 3,          // output of join
	CROSS_PRODUCT = 4, // out of cartesian product
	TABLE_FUNCTION = 5 // table producing function
};

} // namespace duckdb
