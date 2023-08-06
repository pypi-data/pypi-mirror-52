#include "catalog/catalog_entry/view_catalog_entry.hpp"
#include "main/client_context.hpp"
#include "main/database.hpp"
#include "parser/tableref/basetableref.hpp"
#include "parser/tableref/subqueryref.hpp"
#include "planner/binder.hpp"
#include "planner/tableref/bound_basetableref.hpp"
#include "planner/tableref/bound_subqueryref.hpp"

using namespace duckdb;
using namespace std;

unique_ptr<BoundTableRef> Binder::Bind(BaseTableRef &expr) {
	// CTEs and views are also referred to using BaseTableRefs, hence need to distinguish here
	// check if the table name refers to a CTE
	auto cte = FindCTE(expr.table_name);
	if (cte) {
		// it does! create a subquery with a copy of the CTE and resolve it
		SubqueryRef subquery(move(cte));
		subquery.alias = expr.alias.empty() ? expr.table_name : expr.alias;
		return Bind(subquery);
	}
	// not a CTE
	// extract a table or view from the catalog
	auto table_or_view = context.catalog.GetTableOrView(context.ActiveTransaction(), expr.schema_name, expr.table_name);
	switch (table_or_view->type) {
	case CatalogType::TABLE: {
		// base table: create the BoundBaseTableRef node
		auto table = (TableCatalogEntry *)table_or_view;
		auto table_index = GenerateTableIndex();
		auto result = make_unique<BoundBaseTableRef>(table, table_index);
		bind_context.AddBaseTable(result.get(), expr.alias.empty() ? expr.table_name : expr.alias);
		return move(result);
	}
	case CatalogType::VIEW: {
		// the node is a view: get the query that the view represents
		auto view_catalog_entry = (ViewCatalogEntry *)table_or_view;
		SubqueryRef subquery(view_catalog_entry->query->Copy());
		subquery.alias = expr.alias.empty() ? expr.table_name : expr.alias;
		subquery.column_name_alias = view_catalog_entry->aliases;
		// bind the child subquery
		return Bind(subquery);
	}
	default:
		throw NotImplementedException("Catalog entry type");
	}
}
