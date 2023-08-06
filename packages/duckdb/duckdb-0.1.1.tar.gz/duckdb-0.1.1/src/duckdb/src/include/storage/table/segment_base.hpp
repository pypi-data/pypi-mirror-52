//===----------------------------------------------------------------------===//
//                         DuckDB
//
// storage/table/segment_base.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/constants.hpp"

namespace duckdb {

class SegmentBase {
public:
	SegmentBase(index_t start, index_t count) : start(start), count(count) {
	}
	virtual ~SegmentBase() {
	}

	//! The start row id of this chunk
	index_t start;
	//! The amount of entries in this storage chunk
	index_t count;
	//! The next segment after this one
	unique_ptr<SegmentBase> next;
};

} // namespace duckdb
