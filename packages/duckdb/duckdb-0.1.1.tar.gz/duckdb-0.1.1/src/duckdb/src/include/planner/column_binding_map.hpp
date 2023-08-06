//===----------------------------------------------------------------------===//
//                         DuckDB
//
// planner/column_binding_map.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/types/hash.hpp"
#include "common/unordered_map.hpp"
#include "planner/column_binding.hpp"

namespace duckdb {

struct ColumnBindingHashFunction {
	uint64_t operator()(const ColumnBinding &a) const {
		return CombineHash(Hash<index_t>(a.table_index), Hash<index_t>(a.column_index));
	}
};

struct ColumnBindingEquality {
	bool operator()(const ColumnBinding &a, const ColumnBinding &b) const {
		return a == b;
	}
};

template <typename T>
using column_binding_map_t = unordered_map<ColumnBinding, T, ColumnBindingHashFunction, ColumnBindingEquality>;

} // namespace duckdb
