#include "main/query_result.hpp"

#include "main/client_context.hpp"

using namespace duckdb;
using namespace std;

QueryResult::QueryResult(QueryResultType type, StatementType statement_type)
    : type(type), statement_type(statement_type), success(true) {
}

QueryResult::QueryResult(QueryResultType type, StatementType statement_type, vector<SQLType> sql_types,
                         vector<TypeId> types, vector<string> names)
    : type(type), statement_type(statement_type), sql_types(sql_types), types(types), names(names), success(true) {
	assert(types.size() == names.size());
}

QueryResult::QueryResult(QueryResultType type, string error) : type(type), success(false), error(error) {
}

bool QueryResult::Equals(QueryResult &other) {
	// first compare the success state of the results
	if (success != other.success) {
		return false;
	}
	if (!success) {
		return error == other.error;
	}
	// compare names
	if (names != other.names) {
		return false;
	}
	// compare types
	if (sql_types != other.sql_types || types != other.types) {
		return false;
	}
	// now compare the actual values
	// fetch chunks
	while (true) {
		auto lchunk = Fetch();
		auto rchunk = other.Fetch();
		if (lchunk->size() == 0 && rchunk->size() == 0) {
			return true;
		}
		if (lchunk->size() != rchunk->size()) {
			return false;
		}
		assert(lchunk->column_count == rchunk->column_count);
		for (index_t col = 0; col < rchunk->column_count; col++) {
			for (index_t row = 0; row < rchunk->size(); row++) {
				auto lvalue = lchunk->data[col].GetValue(row);
				auto rvalue = rchunk->data[col].GetValue(row);
				if (lvalue != rvalue) {
					return false;
				}
			}
		}
	}
}

void QueryResult::Print() {
	fprintf(stderr, "%s\n", ToString().c_str());
}

string QueryResult::HeaderToString() {
	string result;
	for (auto &name : names) {
		result += name + "\t";
	}
	result += "\n";
	for (auto &type : types) {
		result += TypeIdToString(type) + "\t";
	}
	result += "\n";
	return result;
}
