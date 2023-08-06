//===----------------------------------------------------------------------===//
//                         DuckDB
//
// execution/index/art/node256.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once
#include "node.hpp"

namespace duckdb {

class Node256 : public Node {
public:
	Node256(ART &art);

	unique_ptr<Node> child[256];

public:
	//! Get position of a specific byte, returns INVALID_INDEX if not exists
	index_t GetChildPos(uint8_t k) override;
	//! Get the position of the first child that is greater or equal to the specific byte, or INVALID_INDEX if there are
	//! no children matching the criteria
	index_t GetChildGreaterEqual(uint8_t k) override;
	//! Get the next position in the node, or INVALID_INDEX if there is no next position
	index_t GetNextPos(index_t pos) override;
	//! Get Node256 Child
	unique_ptr<Node> *GetChild(index_t pos) override;

	//! Insert node From Node256
	static void insert(ART &art, unique_ptr<Node> &node, uint8_t keyByte, unique_ptr<Node> &child);

	//! Shrink to node 48
	static void erase(ART &art, unique_ptr<Node> &node, int pos);
};
} // namespace duckdb
