#include "catalog/catalog_entry/sequence_catalog_entry.hpp"

#include "catalog/catalog_entry/schema_catalog_entry.hpp"
#include "common/exception.hpp"
#include "common/serializer.hpp"
#include "parser/parsed_data/create_sequence_info.hpp"

#include <algorithm>

using namespace duckdb;
using namespace std;

SequenceCatalogEntry::SequenceCatalogEntry(Catalog *catalog, SchemaCatalogEntry *schema, CreateSequenceInfo *info)
    : CatalogEntry(CatalogType::SEQUENCE, catalog, info->name), schema(schema), usage_count(info->usage_count),
      counter(info->start_value), increment(info->increment), start_value(info->start_value),
      min_value(info->min_value), max_value(info->max_value), cycle(info->cycle) {
}

void SequenceCatalogEntry::Serialize(Serializer &serializer) {
	serializer.WriteString(schema->name);
	serializer.WriteString(name);
	// serializer.Write<int64_t>(counter);
	serializer.Write<uint64_t>(usage_count);
	serializer.Write<int64_t>(increment);
	serializer.Write<int64_t>(min_value);
	serializer.Write<int64_t>(max_value);
	serializer.Write<int64_t>(counter);
	serializer.Write<bool>(cycle);
}

unique_ptr<CreateSequenceInfo> SequenceCatalogEntry::Deserialize(Deserializer &source) {
	auto info = make_unique<CreateSequenceInfo>();
	info->schema = source.Read<string>();
	info->name = source.Read<string>();
	// info->counter = source.Read<int64_t>();
	info->usage_count = source.Read<uint64_t>();
	info->increment = source.Read<int64_t>();
	info->min_value = source.Read<int64_t>();
	info->max_value = source.Read<int64_t>();
	info->start_value = source.Read<int64_t>();
	info->cycle = source.Read<bool>();
	return info;
}
