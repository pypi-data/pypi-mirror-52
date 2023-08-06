//===----------------------------------------------------------------------===//
//                         DuckDB
//
// parser/tableref/joinref.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/enums/join_type.hpp"
#include "common/unordered_set.hpp"
#include "parser/parsed_expression.hpp"
#include "parser/tableref.hpp"

namespace duckdb {
//! Represents a JOIN between two expressions
class JoinRef : public TableRef {
public:
	JoinRef() : TableRef(TableReferenceType::JOIN) {
	}

	//! The left hand side of the join
	unique_ptr<TableRef> left;
	//! The right hand side of the join
	unique_ptr<TableRef> right;
	//! The join condition
	unique_ptr<ParsedExpression> condition;
	//! The join type
	JoinType type;
	//! Columns hidden from SELECT * expansion (because of USING clause)
	unordered_set<string> hidden_columns;

public:
	bool Equals(const TableRef *other_) const override;

	unique_ptr<TableRef> Copy() override;

	//! Serializes a blob into a JoinRef
	void Serialize(Serializer &serializer) override;
	//! Deserializes a blob back into a JoinRef
	static unique_ptr<TableRef> Deserialize(Deserializer &source);
};
} // namespace duckdb
