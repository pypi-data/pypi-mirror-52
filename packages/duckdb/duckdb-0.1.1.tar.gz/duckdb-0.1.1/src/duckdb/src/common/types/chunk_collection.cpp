#include "common/types/chunk_collection.hpp"

#include "common/exception.hpp"
#include "common/printer.hpp"
#include "common/value_operations/value_operations.hpp"

#include <algorithm>
#include <cstring>

using namespace duckdb;
using namespace std;

void ChunkCollection::Append(DataChunk &new_chunk) {
	if (new_chunk.size() == 0) {
		return;
	}
	// we have to ensure that every chunk in the ChunkCollection is completely
	// filled, otherwise our O(1) lookup in GetValue and SetValue does not work
	// first fill the latest chunk, if it exists
	count += new_chunk.size();

	index_t remaining_data = new_chunk.size();
	index_t offset = 0;
	if (chunks.size() == 0) {
		// first chunk
		types = new_chunk.GetTypes();
	} else {
#ifdef DEBUG
		// the types of the new chunk should match the types of the previous one
		assert(types.size() == new_chunk.column_count);
		auto new_types = new_chunk.GetTypes();
		for (index_t i = 0; i < types.size(); i++) {
			assert(new_types[i] == types[i]);
		}
#endif

		// first append data to the current chunk
		DataChunk &last_chunk = *chunks.back();
		index_t added_data = std::min(remaining_data, (index_t)(STANDARD_VECTOR_SIZE - last_chunk.size()));
		if (added_data > 0) {
			// copy <added_data> elements to the last chunk
			index_t old_count = new_chunk.size();
			for (index_t c = 0; c < new_chunk.column_count; c++) {
				new_chunk.data[c].count = added_data;
			}
			last_chunk.Append(new_chunk);
			remaining_data -= added_data;
			// reset the chunk to the old data
			for (index_t c = 0; c < new_chunk.column_count; c++) {
				new_chunk.data[c].count = old_count;
			}
			offset = added_data;
		}
	}

	if (remaining_data > 0) {
		// create a new chunk and fill it with the remainder
		auto chunk = make_unique<DataChunk>();
		chunk->Initialize(types);
		new_chunk.Copy(*chunk, offset);
		chunks.push_back(move(chunk));
	}
}

// returns an int similar to a C comparator:
// -1 if left < right
// 0 if left == right
// 1 if left > right

template <class TYPE>
static int8_t templated_compare_value(Vector &left_vec, Vector &right_vec, index_t left_idx, index_t right_idx) {
	assert(left_vec.type == right_vec.type);
	TYPE left_val = ((TYPE *)left_vec.data)[left_idx];
	TYPE right_val = ((TYPE *)right_vec.data)[right_idx];
	if (left_val == right_val) {
		return 0;
	}
	if (left_val < right_val) {
		return -1;
	}
	return 1;
}

static int8_t compare_value(Vector &left_vec, Vector &right_vec, index_t vector_idx_left, index_t vector_idx_right) {

	auto left_null = left_vec.nullmask[vector_idx_left];
	auto right_null = right_vec.nullmask[vector_idx_right];

	if (left_null && right_null) {
		return 0;
	} else if (right_null) {
		return 1;
	} else if (left_null) {
		return -1;
	}

	switch (left_vec.type) {
	case TypeId::BOOLEAN:
	case TypeId::TINYINT:
		return templated_compare_value<int8_t>(left_vec, right_vec, vector_idx_left, vector_idx_right);
	case TypeId::SMALLINT:
		return templated_compare_value<int16_t>(left_vec, right_vec, vector_idx_left, vector_idx_right);
	case TypeId::INTEGER:
		return templated_compare_value<int32_t>(left_vec, right_vec, vector_idx_left, vector_idx_right);
	case TypeId::BIGINT:
		return templated_compare_value<int64_t>(left_vec, right_vec, vector_idx_left, vector_idx_right);
	case TypeId::FLOAT:
		return templated_compare_value<float>(left_vec, right_vec, vector_idx_left, vector_idx_right);
	case TypeId::DOUBLE:
		return templated_compare_value<double>(left_vec, right_vec, vector_idx_left, vector_idx_right);
	case TypeId::VARCHAR:
		return strcmp(((char **)left_vec.data)[vector_idx_left], ((char **)right_vec.data)[vector_idx_right]);
	default:
		throw NotImplementedException("Type for comparison");
	}
	return false;
}

static int compare_tuple(ChunkCollection *sort_by, vector<OrderType> &desc, index_t left, index_t right) {
	assert(sort_by);

	index_t chunk_idx_left = left / STANDARD_VECTOR_SIZE;
	index_t chunk_idx_right = right / STANDARD_VECTOR_SIZE;
	index_t vector_idx_left = left % STANDARD_VECTOR_SIZE;
	index_t vector_idx_right = right % STANDARD_VECTOR_SIZE;

	auto &left_chunk = sort_by->chunks[chunk_idx_left];
	auto &right_chunk = sort_by->chunks[chunk_idx_right];

	for (index_t col_idx = 0; col_idx < desc.size(); col_idx++) {
		auto order_type = desc[col_idx];

		Vector &left_vec = left_chunk->data[col_idx];
		Vector &right_vec = right_chunk->data[col_idx];

		assert(!left_vec.sel_vector);
		assert(!right_vec.sel_vector);
		assert(left_vec.type == right_vec.type);

		auto comp_res = compare_value(left_vec, right_vec, vector_idx_left, vector_idx_right);

		if (comp_res == 0) {
			continue;
		}
		return comp_res < 0 ? (order_type == OrderType::ASCENDING ? -1 : 1)
		                    : (order_type == OrderType::ASCENDING ? 1 : -1);
	}
	return 0;
}

static int64_t _quicksort_initial(ChunkCollection *sort_by, vector<OrderType> &desc, index_t *result) {
	// select pivot
	int64_t pivot = 0;
	int64_t low = 0, high = sort_by->count - 1;
	// now insert elements
	for (index_t i = 1; i < sort_by->count; i++) {
		if (compare_tuple(sort_by, desc, i, pivot) <= 0) {
			result[low++] = i;
		} else {
			result[high--] = i;
		}
	}
	assert(low == high);
	result[low] = pivot;
	return low;
}

static void _quicksort_inplace(ChunkCollection *sort_by, vector<OrderType> &desc, index_t *result, int64_t left,
                               int64_t right) {
	if (left >= right) {
		return;
	}

	int64_t middle = left + (right - left) / 2;
	int64_t pivot = result[middle];
	// move the mid point value to the front.
	int64_t i = left + 1;
	int64_t j = right;

	std::swap(result[middle], result[left]);
	while (i <= j) {
		while (i <= j && compare_tuple(sort_by, desc, result[i], pivot) <= 0) {
			i++;
		}

		while (i <= j && compare_tuple(sort_by, desc, result[j], pivot) > 0) {
			j--;
		}

		if (i < j) {
			std::swap(result[i], result[j]);
		}
	}
	std::swap(result[i - 1], result[left]);
	int64_t part = i - 1;

	_quicksort_inplace(sort_by, desc, result, left, part - 1);
	_quicksort_inplace(sort_by, desc, result, part + 1, right);
}

void ChunkCollection::Sort(vector<OrderType> &desc, index_t result[]) {
	assert(result);
	if (count == 0)
		return;
	// quicksort
	int64_t part = _quicksort_initial(this, desc, result);
	_quicksort_inplace(this, desc, result, 0, part);
	_quicksort_inplace(this, desc, result, part + 1, count - 1);
}

// FIXME make this more efficient by not using the Value API
// just use memcpy in the vectors
// assert that there is no selection list
void ChunkCollection::Reorder(index_t order_org[]) {
	auto order = unique_ptr<index_t[]>(new index_t[count]);
	memcpy(order.get(), order_org, sizeof(index_t) * count);

	// adapted from https://stackoverflow.com/a/7366196/2652376

	auto val_buf = vector<Value>();
	val_buf.resize(column_count());

	index_t j, k;
	for (index_t i = 0; i < count; i++) {
		for (index_t col_idx = 0; col_idx < column_count(); col_idx++) {
			val_buf[col_idx] = GetValue(col_idx, i);
		}
		j = i;
		while (true) {
			k = order[j];
			order[j] = j;
			if (k == i) {
				break;
			}
			for (index_t col_idx = 0; col_idx < column_count(); col_idx++) {
				SetValue(col_idx, j, GetValue(col_idx, k));
			}
			j = k;
		}
		for (index_t col_idx = 0; col_idx < column_count(); col_idx++) {
			SetValue(col_idx, j, val_buf[col_idx]);
		}
	}
}

template <class TYPE>
static void templated_set_values(ChunkCollection *src_coll, Vector &tgt_vec, index_t order[], index_t col_idx,
                                 index_t start_offset, index_t remaining_data) {
	assert(src_coll);

	for (index_t row_idx = 0; row_idx < remaining_data; row_idx++) {
		index_t chunk_idx_src = order[start_offset + row_idx] / STANDARD_VECTOR_SIZE;
		index_t vector_idx_src = order[start_offset + row_idx] % STANDARD_VECTOR_SIZE;

		auto &src_chunk = src_coll->chunks[chunk_idx_src];
		Vector &src_vec = src_chunk->data[col_idx];

		tgt_vec.nullmask[row_idx] = src_vec.nullmask[vector_idx_src];
		if (tgt_vec.nullmask[row_idx]) {
			continue;
		}
		((TYPE *)tgt_vec.data)[row_idx] = ((TYPE *)src_vec.data)[vector_idx_src];
	}
}

// TODO: reorder functionality is similar, perhaps merge
void ChunkCollection::MaterializeSortedChunk(DataChunk &target, index_t order[], index_t start_offset) {
	index_t remaining_data = min((index_t)STANDARD_VECTOR_SIZE, count - start_offset);
	assert(target.GetTypes() == types);

	for (index_t col_idx = 0; col_idx < column_count(); col_idx++) {
		target.data[col_idx].count = remaining_data;

		switch (types[col_idx]) {
		case TypeId::BOOLEAN:
		case TypeId::TINYINT:
			templated_set_values<int8_t>(this, target.data[col_idx], order, col_idx, start_offset, remaining_data);
			break;
		case TypeId::SMALLINT:
			templated_set_values<int16_t>(this, target.data[col_idx], order, col_idx, start_offset, remaining_data);
			break;
		case TypeId::INTEGER:
			templated_set_values<int32_t>(this, target.data[col_idx], order, col_idx, start_offset, remaining_data);
			break;
		case TypeId::BIGINT:
			templated_set_values<int64_t>(this, target.data[col_idx], order, col_idx, start_offset, remaining_data);
			break;
		case TypeId::FLOAT:
			templated_set_values<float>(this, target.data[col_idx], order, col_idx, start_offset, remaining_data);
			break;
		case TypeId::DOUBLE:
			templated_set_values<double>(this, target.data[col_idx], order, col_idx, start_offset, remaining_data);
			break;
		case TypeId::VARCHAR:
			templated_set_values<char *>(this, target.data[col_idx], order, col_idx, start_offset, remaining_data);
			break;
		default:
			throw NotImplementedException("Type for setting");
		}
	}
	target.Verify();
}

Value ChunkCollection::GetValue(index_t column, index_t index) {
	return chunks[LocateChunk(index)]->data[column].GetValue(index % STANDARD_VECTOR_SIZE);
}

vector<Value> ChunkCollection::GetRow(index_t index) {
	vector<Value> values;
	values.resize(column_count());

	for (index_t p_idx = 0; p_idx < column_count(); p_idx++) {
		values[p_idx] = GetValue(p_idx, index);
	}
	return values;
}

void ChunkCollection::SetValue(index_t column, index_t index, Value value) {
	chunks[LocateChunk(index)]->data[column].SetValue(index % STANDARD_VECTOR_SIZE, value);
}

void ChunkCollection::Print() {
	Printer::Print(ToString());
}

bool ChunkCollection::Equals(ChunkCollection &other) {
	if (count != other.count) {
		return false;
	}
	if (column_count() != other.column_count()) {
		return false;
	}
	if (types != other.types) {
		return false;
	}
	// if count is equal amount of chunks should be equal
	for (index_t row_idx = 0; row_idx < count; row_idx++) {
		for (index_t col_idx = 0; col_idx < column_count(); col_idx++) {
			auto lvalue = GetValue(col_idx, row_idx);
			auto rvalue = other.GetValue(col_idx, row_idx);
			if (!Value::ValuesAreEqual(lvalue, rvalue)) {
				return false;
			}
		}
	}
	return true;
}
