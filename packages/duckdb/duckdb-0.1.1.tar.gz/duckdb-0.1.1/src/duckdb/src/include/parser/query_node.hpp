//===----------------------------------------------------------------------===//
//                         DuckDB
//
// parser/query_node.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

#include "common/common.hpp"
#include "common/enums/order_type.hpp"
#include "common/serializer.hpp"
#include "parser/parsed_expression.hpp"

namespace duckdb {

enum QueryNodeType : uint8_t { SELECT_NODE = 1, SET_OPERATION_NODE = 2 };

//! Single node in ORDER BY statement
struct OrderByNode {
	OrderByNode() {
	}
	OrderByNode(OrderType type, unique_ptr<ParsedExpression> expression) : type(type), expression(move(expression)) {
	}

	//! Sort order, ASC or DESC
	OrderType type;
	//! Expression to order by
	unique_ptr<ParsedExpression> expression;
};

class QueryNode {
public:
	QueryNode(QueryNodeType type) : type(type) {
	}
	virtual ~QueryNode() {
	}

	//! The type of the query node, either SetOperation or Select
	QueryNodeType type;
	//! DISTINCT or not
	bool select_distinct = false;
	//! List of order nodes
	vector<OrderByNode> orders;
	//! LIMIT count
	unique_ptr<ParsedExpression> limit;
	//! OFFSET
	unique_ptr<ParsedExpression> offset;

	virtual const vector<unique_ptr<ParsedExpression>> &GetSelectList() const = 0;

public:
	virtual bool Equals(const QueryNode *other) const;

	//! Create a copy of this QueryNode
	virtual unique_ptr<QueryNode> Copy() = 0;
	//! Serializes a QueryNode to a stand-alone binary blob
	virtual void Serialize(Serializer &serializer);
	//! Deserializes a blob back into a QueryNode, returns nullptr if
	//! deserialization is not possible
	static unique_ptr<QueryNode> Deserialize(Deserializer &source);

protected:
	void CopyProperties(QueryNode &other);
};

}; // namespace duckdb
