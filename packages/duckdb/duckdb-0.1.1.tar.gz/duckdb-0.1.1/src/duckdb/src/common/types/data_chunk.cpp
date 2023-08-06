#include "common/types/data_chunk.hpp"

#include "common/exception.hpp"
#include "common/helper.hpp"
#include "common/printer.hpp"
#include "common/serializer.hpp"
#include "common/types/null_value.hpp"
#include "common/vector_operations/vector_operations.hpp"

using namespace duckdb;
using namespace std;

DataChunk::DataChunk() : column_count(0), data(nullptr), sel_vector(nullptr) {
}

void DataChunk::InitializeEmpty(vector<TypeId> &types) {
	assert(types.size() > 0);
	column_count = types.size();
	data = unique_ptr<Vector[]>(new Vector[types.size()]);
	for (index_t i = 0; i < types.size(); i++) {
		data[i].type = types[i];
		data[i].data = nullptr;
		data[i].count = 0;
		data[i].sel_vector = nullptr;
	}
}

void DataChunk::Initialize(vector<TypeId> &types, bool zero_data) {
	assert(types.size() > 0);
	InitializeEmpty(types);
	index_t size = 0;
	for (auto &type : types) {
		size += GetTypeIdSize(type) * STANDARD_VECTOR_SIZE;
	}
	assert(size > 0);
	owned_data = unique_ptr<data_t[]>(new data_t[size]);
	if (zero_data) {
		memset(owned_data.get(), 0, size);
	}

	auto ptr = owned_data.get();
	for (index_t i = 0; i < types.size(); i++) {
		data[i].data = ptr;
		ptr += GetTypeIdSize(types[i]) * STANDARD_VECTOR_SIZE;
	}
}

void DataChunk::Reset() {
	auto ptr = owned_data.get();
	for (index_t i = 0; i < column_count; i++) {
		data[i].data = ptr;
		data[i].count = 0;
		data[i].sel_vector = nullptr;
		data[i].owned_data = nullptr;
		data[i].string_heap.Destroy();
		data[i].nullmask.reset();
		ptr += GetTypeIdSize(data[i].type) * STANDARD_VECTOR_SIZE;
	}
	sel_vector = nullptr;
}

void DataChunk::Destroy() {
	data = nullptr;
	owned_data.reset();
	sel_vector = nullptr;
	column_count = 0;
}

void DataChunk::Copy(DataChunk &other, index_t offset) {
	assert(column_count == other.column_count);
	other.sel_vector = nullptr;

	for (index_t i = 0; i < column_count; i++) {
		data[i].Copy(other.data[i], offset);
	}
}

void DataChunk::Move(DataChunk &other) {
	other.column_count = column_count;
	other.data = move(data);
	other.owned_data = move(owned_data);
	if (sel_vector) {
		other.sel_vector = sel_vector;
		if (sel_vector == owned_sel_vector) {
			// copy the owned selection vector
			memcpy(other.owned_sel_vector, owned_sel_vector, STANDARD_VECTOR_SIZE * sizeof(sel_t));
		}
	}
	Destroy();
}

void DataChunk::Flatten() {
	if (!sel_vector) {
		return;
	}

	for (index_t i = 0; i < column_count; i++) {
		data[i].Flatten();
	}
	sel_vector = nullptr;
}

void DataChunk::Append(DataChunk &other) {
	if (other.size() == 0) {
		return;
	}
	if (column_count != other.column_count) {
		throw OutOfRangeException("Column counts of appending chunk doesn't match!");
	}
	for (index_t i = 0; i < column_count; i++) {
		data[i].Append(other.data[i]);
	}
}

void DataChunk::MergeSelVector(sel_t *current_vector, sel_t *new_vector, sel_t *result, index_t new_count) {
	for (index_t i = 0; i < new_count; i++) {
		result[i] = current_vector[new_vector[i]];
	}
}

void DataChunk::SetSelectionVector(Vector &matches) {
	if (matches.type != TypeId::BOOLEAN) {
		throw InvalidTypeException(matches.type, "Can only set selection vector using a boolean vector!");
	}
	bool *match_data = (bool *)matches.data;
	index_t match_count = 0;
	if (sel_vector) {
		assert(matches.sel_vector);
		// existing selection vector: have to merge the selection vector
		for (index_t i = 0; i < matches.count; i++) {
			if (match_data[sel_vector[i]] && !matches.nullmask[sel_vector[i]]) {
				owned_sel_vector[match_count++] = sel_vector[i];
			}
		}
		sel_vector = owned_sel_vector;
	} else {
		// no selection vector yet: can just set the selection vector
		for (index_t i = 0; i < matches.count; i++) {
			if (match_data[i] && !matches.nullmask[i]) {
				owned_sel_vector[match_count++] = i;
			}
		}
		if (match_count < matches.count) {
			// we only have to set the selection vector if tuples were filtered
			sel_vector = owned_sel_vector;
		}
	}
	for (index_t i = 0; i < column_count; i++) {
		data[i].count = match_count;
		data[i].sel_vector = sel_vector;
	}
}

vector<TypeId> DataChunk::GetTypes() {
	vector<TypeId> types;
	for (index_t i = 0; i < column_count; i++) {
		types.push_back(data[i].type);
	}
	return types;
}

string DataChunk::ToString() const {
	string retval = "Chunk - [" + to_string(column_count) + " Columns]\n";
	for (index_t i = 0; i < column_count; i++) {
		retval += "- " + data[i].ToString() + "\n";
	}
	return retval;
}

void DataChunk::Serialize(Serializer &serializer) {
	// write the count
	serializer.Write<sel_t>(size());
	serializer.Write<index_t>(column_count);
	for (index_t i = 0; i < column_count; i++) {
		// write the types
		serializer.Write<int>((int)data[i].type);
	}
	// write the data
	for (index_t i = 0; i < column_count; i++) {
		auto type = data[i].type;
		if (TypeIsConstantSize(type)) {
			index_t write_size = GetTypeIdSize(type) * size();
			auto ptr = unique_ptr<data_t[]>(new data_t[write_size]);
			// constant size type: simple memcpy
			VectorOperations::CopyToStorage(data[i], ptr.get());
			serializer.WriteData(ptr.get(), write_size);
		} else {
			assert(type == TypeId::VARCHAR);
			// strings are inlined into the blob
			// we use null-padding to store them
			auto strings = (const char **)data[i].data;
			for (index_t j = 0; j < size(); j++) {
				auto source = strings[j] ? strings[j] : NullValue<const char *>();
				serializer.WriteString(source);
			}
		}
	}
}

void DataChunk::Deserialize(Deserializer &source) {
	auto rows = source.Read<sel_t>();
	column_count = source.Read<index_t>();

	vector<TypeId> types;
	for (index_t i = 0; i < column_count; i++) {
		types.push_back((TypeId)source.Read<int>());
	}
	Initialize(types);
	// now load the column data
	for (index_t i = 0; i < column_count; i++) {
		auto type = data[i].type;
		if (TypeIsConstantSize(type)) {
			// constant size type: simple memcpy
			auto column_size = GetTypeIdSize(type) * rows;
			auto ptr = unique_ptr<data_t[]>(new data_t[column_size]);
			source.ReadData(ptr.get(), column_size);
			Vector v(data[i].type, ptr.get());
			v.count = rows;
			VectorOperations::AppendFromStorage(v, data[i]);
		} else {
			auto strings = (const char **)data[i].data;
			for (index_t j = 0; j < rows; j++) {
				// read the strings
				auto str = source.Read<string>();
				// now add the string to the StringHeap of the vector
				// and write the pointer into the vector
				if (IsNullValue<const char *>((const char *)str.c_str())) {
					strings[j] = nullptr;
					data[i].nullmask[j] = true;
				} else {
					strings[j] = data[i].string_heap.AddString(str);
				}
			}
		}
		data[i].count = rows;
	}
	Verify();
}

void DataChunk::MoveStringsToHeap(StringHeap &heap) {
	for (index_t c = 0; c < column_count; c++) {
		if (data[c].type == TypeId::VARCHAR) {
			// move strings of this chunk to the specified heap
			auto source_strings = (const char **)data[c].data;
			if (!data[c].owned_data) {
				data[c].owned_data = unique_ptr<data_t[]>(new data_t[STANDARD_VECTOR_SIZE * sizeof(data_ptr_t)]);
				data[c].data = data[c].owned_data.get();
			}
			auto target_strings = (const char **)data[c].data;
			VectorOperations::ExecType<const char *>(data[c], [&](const char *str, index_t i, index_t k) {
				if (!data[c].nullmask[i]) {
					target_strings[i] = heap.AddString(source_strings[i]);
				}
			});
		}
	}
}

void DataChunk::Hash(Vector &result) {
	assert(result.type == TypeId::HASH);
	VectorOperations::Hash(data[0], result);
	for (index_t i = 1; i < column_count; i++) {
		VectorOperations::CombineHash(result, data[i]);
	}
}

void DataChunk::Verify() {
#ifdef DEBUG
	// verify that all vectors in this chunk have the chunk selection vector
	sel_t *v = sel_vector;
	for (index_t i = 0; i < column_count; i++) {
		assert(data[i].sel_vector == v);
		data[i].Verify();
	}
	// verify that all vectors in the chunk have the same count
	for (index_t i = 0; i < column_count; i++) {
		assert(size() == data[i].count);
	}
#endif
}

void DataChunk::Print() {
	Printer::Print(ToString());
}
