#include "parser/tableref/basetableref.hpp"
#include "parser/transformer.hpp"

using namespace duckdb;
using namespace postgres;
using namespace std;

unique_ptr<TableRef> Transformer::TransformRangeVar(RangeVar *root) {
	auto result = make_unique<BaseTableRef>();

	result->alias = TransformAlias(root->alias);
	if (root->relname)
		result->table_name = root->relname;
	if (root->schemaname)
		result->schema_name = root->schemaname;
	return move(result);
}
