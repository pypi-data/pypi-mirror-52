#include "function/scalar/string_functions.hpp"
#include "common/exception.hpp"
#include "common/vector_operations/vector_operations.hpp"
#include "execution/expression_executor.hpp"
#include "planner/expression/bound_function_expression.hpp"

#include "re2/re2.h"

using namespace re2;
using namespace std;

namespace duckdb {

RegexpMatchesBindData::RegexpMatchesBindData(unique_ptr<RE2> constant_pattern, string range_min, string range_max, bool range_success)
        : constant_pattern(std::move(constant_pattern)), range_min(range_min), range_max(range_max),
          range_success(range_success) {
}

RegexpMatchesBindData::~RegexpMatchesBindData() {
}

unique_ptr<FunctionData> RegexpMatchesBindData::Copy() {
	return make_unique<RegexpMatchesBindData>(move(constant_pattern), range_min, range_max, range_success);
}

static void regexp_matches_function(ExpressionExecutor &exec, Vector inputs[], index_t input_count,
                             BoundFunctionExpression &expr, Vector &result) {
	assert(input_count == 2);
	auto &strings = inputs[0];
	auto &patterns = inputs[1];

	auto &info = (RegexpMatchesBindData &)*expr.bind_info;

	assert(strings.type == TypeId::VARCHAR);
	assert(patterns.type == TypeId::VARCHAR);

	result.Initialize(TypeId::BOOLEAN);
	result.nullmask = strings.nullmask | patterns.nullmask;

	auto strings_data = (const char **)strings.data;
	auto patterns_data = (const char **)patterns.data;
	auto result_data = (bool *)result.data;

	RE2::Options options;
	options.set_log_errors(false);

	VectorOperations::BinaryExec(strings, patterns, result,
	                             [&](index_t strings_index, index_t patterns_index, index_t result_index) {
		                             if (result.nullmask[result_index]) {
			                             return;
		                             }
		                             auto string = strings_data[strings_index];

		                             if (info.constant_pattern) {
			                             result_data[result_index] = RE2::PartialMatch(string, *info.constant_pattern);

		                             } else {
			                             auto pattern = patterns_data[patterns_index];
			                             RE2 re(pattern, options);

			                             if (!re.ok()) {
				                             throw Exception(re.error());
			                             }
			                             result_data[result_index] = RE2::PartialMatch(string, re);
		                             }
	                             });
}

static unique_ptr<FunctionData> regexp_matches_get_bind_function(BoundFunctionExpression &expr, ClientContext &context) {
	// pattern is the second argument. If its constant, we can already prepare the pattern and store it for later.
	assert(expr.children.size() == 2);
	if (expr.children[1]->IsScalar()) {
		Value pattern_str = ExpressionExecutor::EvaluateScalar(*expr.children[1]);
		if (!pattern_str.is_null && pattern_str.type == TypeId::VARCHAR) {
			RE2::Options options;
			options.set_log_errors(false);
			auto re = make_unique<RE2>(pattern_str.str_value, options);
			if (!re->ok()) {
				throw Exception(re->error());
			}

			string range_min, range_max;
			auto range_success = re->PossibleMatchRange(&range_min, &range_max, 1000);
			// range_min and range_max might produce non-valid UTF8 strings, e.g. in the case of 'a.*'
			// in this case we don't push a range filter
			if (range_success && (!Value::IsUTF8String(range_min.c_str()) || !Value::IsUTF8String(range_max.c_str()))) {
				range_success = false;
			}

			return make_unique<RegexpMatchesBindData>(move(re), range_min, range_max, range_success);
		}
	}
	return make_unique<RegexpMatchesBindData>(nullptr, "", "", false);
}

static void regexp_replace_function(ExpressionExecutor &exec, Vector inputs[], index_t input_count,
                             BoundFunctionExpression &expr, Vector &result) {
	assert(input_count == 3);
	auto &strings = inputs[0];
	auto &patterns = inputs[1];
	auto &replaces = inputs[2];

	assert(strings.type == TypeId::VARCHAR);
	assert(patterns.type == TypeId::VARCHAR);
	assert(replaces.type == TypeId::VARCHAR);

	result.Initialize(TypeId::VARCHAR);
	result.nullmask =
	    strings.nullmask | patterns.nullmask | replaces.nullmask; // TODO what would jesus, err postgres do

	auto strings_data = (const char **)strings.data;
	auto patterns_data = (const char **)patterns.data;
	auto replaces_data = (const char **)replaces.data;
	auto result_data = (const char **)result.data;

	RE2::Options options;
	options.set_log_errors(false);

	VectorOperations::TernaryExec(
	    strings, patterns, replaces, result,
	    [&](index_t strings_index, index_t patterns_index, index_t replaces_index, index_t result_index) {
		    if (result.nullmask[strings_index]) {
			    return;
		    }

		    auto string = strings_data[strings_index];
		    auto pattern = patterns_data[patterns_index];
		    auto replace = replaces_data[replaces_index];

		    RE2 re(pattern, options);
		    std::string sstring(string);
		    RE2::Replace(&sstring, re, replace);
		    result_data[result_index] = result.string_heap.AddString(sstring.c_str());
	    });
}

void Regexp::RegisterFunction(BuiltinFunctions &set) {
	set.AddFunction(ScalarFunction("regexp_matches", { SQLType::VARCHAR, SQLType::VARCHAR }, SQLType::BOOLEAN, regexp_matches_function, false, regexp_matches_get_bind_function));
	set.AddFunction(ScalarFunction("regexp_replace", { SQLType::VARCHAR, SQLType::VARCHAR, SQLType::VARCHAR }, SQLType::VARCHAR, regexp_replace_function));
}

} // namespace duckdb
