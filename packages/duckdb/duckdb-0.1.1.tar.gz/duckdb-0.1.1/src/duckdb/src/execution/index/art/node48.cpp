#include "execution/index/art/node16.hpp"
#include "execution/index/art/node48.hpp"
#include "execution/index/art/node256.hpp"

using namespace duckdb;

Node48::Node48(ART &art) : Node(art, NodeType::N48) {
	for (uint64_t i = 0; i < 256; i++) {
		childIndex[i] = Node::EMPTY_MARKER;
	}
}

index_t Node48::GetChildPos(uint8_t k) {
	if (childIndex[k] == Node::EMPTY_MARKER) {
		return INVALID_INDEX;
	} else {
		return k;
	}
}

index_t Node48::GetChildGreaterEqual(uint8_t k) {
	for (index_t pos = k; pos < 256; pos++) {
		if (childIndex[pos] != Node::EMPTY_MARKER) {
			return pos;
		}
	}
	return Node::GetChildGreaterEqual(k);
}

index_t Node48::GetNextPos(index_t pos) {
	for (pos == INVALID_INDEX ? pos = 0 : pos++; pos < 256; pos++) {
		if (childIndex[pos] != Node::EMPTY_MARKER) {
			return pos;
		}
	}
	return Node::GetNextPos(pos);
}

unique_ptr<Node> *Node48::GetChild(index_t pos) {
	assert(childIndex[pos] != Node::EMPTY_MARKER);
	return &child[childIndex[pos]];
}

void Node48::insert(ART &art, unique_ptr<Node> &node, uint8_t keyByte, unique_ptr<Node> &child) {
	Node48 *n = static_cast<Node48 *>(node.get());

	// Insert leaf into inner node
	if (node->count < 48) {
		// Insert element
		index_t pos = n->count;
		if (n->child[pos]) {
			// find an empty position in the node list if the current position is occupied
			pos = 0;
			while (n->child[pos]) {
				pos++;
			}
		}
		n->child[pos] = move(child);
		n->childIndex[keyByte] = pos;
		n->count++;
	} else {
		// Grow to Node256
		auto newNode = make_unique<Node256>(art);
		for (index_t i = 0; i < 256; i++) {
			if (n->childIndex[i] != Node::EMPTY_MARKER) {
				newNode->child[i] = move(n->child[n->childIndex[i]]);
			}
		}
		newNode->count = n->count;
		CopyPrefix(art, n, newNode.get());
		node = move(newNode);
		Node256::insert(art, node, keyByte, child);
	}
}

void Node48::erase(ART &art, unique_ptr<Node> &node, int pos) {
	Node48 *n = static_cast<Node48 *>(node.get());

	if (node->count > 12) {
		n->child[n->childIndex[pos]].reset();
		n->childIndex[pos] = Node::EMPTY_MARKER;
		n->count--;
	} else {
		auto newNode = make_unique<Node16>(art);
		CopyPrefix(art, n, newNode.get());
		for (index_t i = 0; i < 256; i++) {
			if (n->childIndex[i] != Node::EMPTY_MARKER) {
				newNode->key[newNode->count] = i;
				newNode->child[newNode->count++] = move(n->child[n->childIndex[i]]);
			}
		}
		node = move(newNode);
	}
}
