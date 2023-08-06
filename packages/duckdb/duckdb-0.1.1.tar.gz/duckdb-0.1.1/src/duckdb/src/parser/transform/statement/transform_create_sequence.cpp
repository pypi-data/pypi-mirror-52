#include "parser/statement/create_sequence_statement.hpp"
#include "parser/tableref/basetableref.hpp"
#include "parser/transformer.hpp"

using namespace duckdb;
using namespace postgres;
using namespace std;

unique_ptr<CreateSequenceStatement> Transformer::TransformCreateSequence(Node *node) {
	auto stmt = reinterpret_cast<CreateSeqStmt *>(node);

	auto result = make_unique<CreateSequenceStatement>();

	auto &info = *result->info;
	auto sequence_name = TransformRangeVar(stmt->sequence);
	auto &sequence_ref = (BaseTableRef &)*sequence_name;
	info.schema = sequence_ref.schema_name;
	info.name = sequence_ref.table_name;

	if (stmt->options) {
		ListCell *cell = nullptr;
		for_each_cell(cell, stmt->options->head) {
			auto *def_elem = reinterpret_cast<DefElem *>(cell->data.ptr_value);
			string opt_name = string(def_elem->defname);

			auto val = (postgres::Value *)def_elem->arg;
			if (def_elem->defaction == DEFELEM_UNSPEC && !val) { // e.g. NO MINVALUE
				continue;
			}
			assert(val);

			if (opt_name == "increment") {
				assert(val->type == T_Integer);
				info.increment = val->val.ival;
				if (info.increment == 0) {
					throw ParserException("Increment must not be zero");
				}
				if (info.increment < 0) {
					info.start_value = info.max_value = -1;
					info.min_value = numeric_limits<int64_t>::min();
				} else {
					info.start_value = info.min_value = 1;
					info.max_value = numeric_limits<int64_t>::max();
				}
			} else if (opt_name == "minvalue") {
				assert(val->type == T_Integer);
				info.min_value = val->val.ival;
				if (info.increment > 0) {
					info.start_value = info.min_value;
				}
			} else if (opt_name == "maxvalue") {
				assert(val->type == T_Integer);
				info.max_value = val->val.ival;
				if (info.increment < 0) {
					info.start_value = info.max_value;
				}
			} else if (opt_name == "start") {
				assert(val->type == T_Integer);
				info.start_value = val->val.ival;
			} else if (opt_name == "cycle") {
				assert(val->type == T_Integer);
				info.cycle = val->val.ival > 0;
			} else {
				throw ParserException("Unrecognized option \"%s\" for CREATE SEQUENCE", opt_name.c_str());
			}
		}
	}
	if (!stmt->sequence->relpersistence) {
		throw ParserException("Temporary sequences are not supported yet");
	}
	info.if_not_exists = stmt->if_not_exists;
	if (info.max_value <= info.min_value) {
		throw ParserException("MINVALUE (%lld) must be less than MAXVALUE (%lld)", info.min_value, info.max_value);
	}
	if (info.start_value < info.min_value) {
		throw ParserException("START value (%lld) cannot be less than MINVALUE (%lld)", info.start_value,
		                      info.min_value);
	}
	if (info.start_value > info.max_value) {
		throw ParserException("START value (%lld) cannot be greater than MAXVALUE (%lld)", info.start_value,
		                      info.max_value);
	}
	return result;
}
