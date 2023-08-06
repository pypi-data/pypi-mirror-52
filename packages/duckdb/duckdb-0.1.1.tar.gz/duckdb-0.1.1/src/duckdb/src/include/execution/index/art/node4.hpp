//===----------------------------------------------------------------------===//
//                         DuckDB
//
// execution/index/art/node4.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once
#include "node.hpp"

namespace duckdb {

class Node4 : public Node {
public:
	Node4(ART &art);

	uint8_t key[4];
	unique_ptr<Node> child[4];

public:
	//! Get position of a byte, returns -1 if not exists
	index_t GetChildPos(uint8_t k) override;
	//! Get the position of the first child that is greater or equal to the specific byte, or INVALID_INDEX if there are
	//! no children matching the criteria
	index_t GetChildGreaterEqual(uint8_t k) override;
	//! Get the next position in the node, or INVALID_INDEX if there is no next position
	index_t GetNextPos(index_t pos) override;
	//! Get Node4 Child
	unique_ptr<Node> *GetChild(index_t pos) override;

	//! Insert Leaf to the Node4
	static void insert(ART &art, unique_ptr<Node> &node, uint8_t keyByte, unique_ptr<Node> &child);
	//! Remove Leaf from Node4
	static void erase(ART &art, unique_ptr<Node> &node, int pos);
};
} // namespace duckdb
