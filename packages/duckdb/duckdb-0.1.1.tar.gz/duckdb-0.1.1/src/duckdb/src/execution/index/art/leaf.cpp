#include "execution/index/art/node.hpp"
#include "execution/index/art/leaf.hpp"

Leaf::Leaf(ART &art, unique_ptr<Key> value, row_t row_id) : Node(art, NodeType::NLeaf) {
	this->value = move(value);
	this->capacity = 1;
	this->row_ids = unique_ptr<row_t[]>(new row_t[this->capacity]);
	this->row_ids[0] = row_id;
	this->num_elements = 1;
}

void Leaf::Insert(row_t row_id) {
	// Grow array
	if (num_elements == capacity) {
		auto new_row_id = unique_ptr<row_t[]>(new row_t[capacity * 2]);
		memcpy(new_row_id.get(), row_ids.get(), capacity * sizeof(row_t));
		capacity *= 2;
		row_ids = move(new_row_id);
	}
	row_ids[num_elements++] = row_id;
}

//! TODO: Maybe shrink array dynamically?
void Leaf::Remove(row_t row_id) {
	index_t entry_offset = -1;
	for (index_t i = 0; i < num_elements; i++) {
		if (row_ids[i] == row_id) {
			entry_offset = i;
			break;
		}
	}
	num_elements--;
	for (index_t j = entry_offset; j < num_elements; j++) {
		row_ids[j] = row_ids[j + 1];
	}
}
