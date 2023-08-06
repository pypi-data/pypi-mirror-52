//===----------------------------------------------------------------------===//
//                         DuckDB
//
// common/serializer/buffered_deserializer.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/serializer/buffered_serializer.hpp"
#include "common/serializer.hpp"

namespace duckdb {

class BufferedDeserializer : public Deserializer {
public:
	BufferedDeserializer(data_ptr_t ptr, index_t data_size);
	BufferedDeserializer(BufferedSerializer &serializer);

	data_ptr_t ptr;
	data_ptr_t endptr;

public:
	void ReadData(data_ptr_t buffer, uint64_t read_size) override;
};

} // namespace duckdb
