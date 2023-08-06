#include "storage/table/segment_tree.hpp"
#include "common/exception.hpp"

using namespace duckdb;
using namespace std;

SegmentBase *SegmentTree::GetRootSegment() {
	return root_node.get();
}

SegmentBase *SegmentTree::GetLastSegment() {
	return nodes.back().node;
}

SegmentBase *SegmentTree::GetSegment(index_t row_number) {
	lock_guard<mutex> tree_lock(node_lock);

	index_t lower = 0;
	index_t upper = nodes.size() - 1;
	// binary search to find the node
	while (lower <= upper) {
		index_t index = (lower + upper) / 2;
		auto &entry = nodes[index];
		if (row_number < entry.row_start) {
			upper = index - 1;
		} else if (row_number >= entry.row_start + entry.node->count) {
			lower = index + 1;
		} else {
			return entry.node;
		}
	}
	throw Exception("Could not find node in column segment tree!");
}

void SegmentTree::AppendSegment(unique_ptr<SegmentBase> segment) {
	// add the node to the list of nodes
	SegmentNode node;
	node.row_start = segment->start;
	node.node = segment.get();
	nodes.push_back(node);

	if (nodes.size() > 1) {
		// add the node as the next pointer of the last node
		nodes[nodes.size() - 2].node->next = move(segment);
	} else {
		root_node = move(segment);
	}
}
