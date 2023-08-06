#include "catalog/catalog_entry/view_catalog_entry.hpp"

#include "catalog/catalog_entry/schema_catalog_entry.hpp"
#include "common/exception.hpp"
#include "common/serializer.hpp"
#include "parser/parsed_data/create_view_info.hpp"

#include <algorithm>

using namespace duckdb;
using namespace std;

void ViewCatalogEntry::Initialize(CreateViewInfo *info) {
	query = move(info->query);
	aliases = info->aliases;
}

ViewCatalogEntry::ViewCatalogEntry(Catalog *catalog, SchemaCatalogEntry *schema, CreateViewInfo *info)
    : CatalogEntry(CatalogType::VIEW, catalog, info->view_name), schema(schema) {
	Initialize(info);
}

void ViewCatalogEntry::Serialize(Serializer &serializer) {
	serializer.WriteString(schema->name);
	serializer.WriteString(name);
	query->Serialize(serializer);
	assert(aliases.size() <= numeric_limits<uint32_t>::max());
	serializer.Write<uint32_t>((uint32_t)aliases.size());
	for (auto &s : aliases) {
		serializer.WriteString(s);
	}
}

unique_ptr<CreateViewInfo> ViewCatalogEntry::Deserialize(Deserializer &source) {
	auto info = make_unique<CreateViewInfo>();
	info->schema = source.Read<string>();
	info->view_name = source.Read<string>();
	info->query = QueryNode::Deserialize(source);
	auto alias_count = source.Read<uint32_t>();
	for (uint32_t i = 0; i < alias_count; i++) {
		info->aliases.push_back(source.Read<string>());
	}
	return info;
}
