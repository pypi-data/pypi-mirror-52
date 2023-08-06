//===----------------------------------------------------------------------===//
//                         DuckDB
//
// execution/window_segment_tree.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/types/chunk_collection.hpp"
#include "execution/physical_operator.hpp"
#include "function/aggregate_function.hpp"

namespace duckdb {

class WindowSegmentTree {
public:
    WindowSegmentTree(AggregateFunction& aggregate, TypeId result_type, ChunkCollection *input);
    Value Compute(index_t start, index_t end);

private:
    void ConstructTree();
    void WindowSegmentValue(index_t l_idx, index_t begin, index_t end);
    void AggregateInit();
    Value AggegateFinal();

    AggregateFunction aggregate;
    vector<data_t> state;
    Vector statep;
    TypeId result_type;
    unique_ptr<data_t[]> levels_flat_native;
    vector<index_t> levels_flat_start;
    unique_ptr<Vector[]> inputs;

    ChunkCollection *input_ref;

    static constexpr index_t TREE_FANOUT = 64; // this should cleanly divide STANDARD_VECTOR_SIZE
};

} // namespace duckdb
