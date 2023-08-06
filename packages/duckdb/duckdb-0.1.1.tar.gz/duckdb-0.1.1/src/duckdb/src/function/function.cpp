#include "function/function.hpp"
#include "function/aggregate_function.hpp"
#include "function/scalar_function.hpp"
#include "function/cast_rules.hpp"

#include "catalog/catalog.hpp"
// #include "function/aggregate/list.hpp"
// #include "function/scalar/list.hpp"
// #include "function/table/list.hpp"
#include "parser/parsed_data/create_aggregate_function_info.hpp"
#include "parser/parsed_data/create_scalar_function_info.hpp"
#include "parser/parsed_data/create_table_function_info.hpp"

using namespace duckdb;
using namespace std;

BuiltinFunctions::BuiltinFunctions(Transaction &transaction, Catalog &catalog) :
	transaction(transaction), catalog(catalog) {
}

void BuiltinFunctions::AddFunction(AggregateFunctionSet set) {
	CreateAggregateFunctionInfo info(set);
	catalog.CreateFunction(transaction, &info);
}

void BuiltinFunctions::AddFunction(AggregateFunction function) {
	CreateAggregateFunctionInfo info(function);
	catalog.CreateFunction(transaction, &info);
}

void BuiltinFunctions::AddFunction(ScalarFunction function) {
	CreateScalarFunctionInfo info(function);
	catalog.CreateFunction(transaction, &info);
}

void BuiltinFunctions::AddFunction(ScalarFunctionSet set) {
	CreateScalarFunctionInfo info(set);
	catalog.CreateFunction(transaction, &info);
}

void BuiltinFunctions::AddFunction(TableFunction function) {
	CreateTableFunctionInfo info(function);
	catalog.CreateTableFunction(transaction, &info);
}

void BuiltinFunctions::Initialize() {
	RegisterSQLiteFunctions();

	RegisterAlgebraicAggregates();
	RegisterDistributiveAggregates();

	RegisterDateFunctions();
	RegisterMathFunctions();
	RegisterOperators();
	RegisterSequenceFunctions();
	RegisterStringFunctions();
	RegisterTrigonometricsFunctions();
}

string Function::CallToString(string name, vector<SQLType> arguments) {
	string result = name + "(";
	for (index_t i = 0; i < arguments.size(); i++) {
		if (i != 0) {
			result += ", ";
		}
		result += SQLTypeToString(arguments[i]);
	}
	return result + ")";
}

string Function::CallToString(string name, vector<SQLType> arguments, SQLType return_type) {
	string result = CallToString(name, arguments);
	result += " -> " + SQLTypeToString(return_type);
	return result;
}

static int64_t BindVarArgsFunctionCost(SimpleFunction &func, vector<SQLType> &arguments) {
	if (arguments.size() < func.arguments.size()) {
		// not enough arguments to fulfill the non-vararg part of the function
		return -1;
	}
	int64_t cost = 0;
	for(index_t i = 0; i < arguments.size(); i++) {
		SQLType arg_type = i < func.arguments.size() ? func.arguments[i] : func.varargs;
		if (arguments[i] == arg_type) {
			// arguments match: do nothing
			continue;
		}
		int64_t cast_cost = CastRules::ImplicitCast(arguments[i], arg_type);
		if (cast_cost >= 0) {
			// we can implicitly cast, add the cost to the total cost
			cost += cast_cost;
		} else {
			// we can't implicitly cast: throw an error
			return -1;
		}
	}
	return cost;
}

static int64_t BindFunctionCost(SimpleFunction &func, vector<SQLType> &arguments) {
	if (func.HasVarArgs()) {
		// special case varargs function
		return BindVarArgsFunctionCost(func, arguments);
	}
	if (func.arguments.size() != arguments.size()) {
		// invalid argument count: check the next function
		return -1;
	}
	int64_t cost = 0;
	for(index_t i = 0; i < arguments.size(); i++) {
		if (arguments[i] == func.arguments[i]) {
			// arguments match: do nothing
			continue;
		}
		int64_t cast_cost = CastRules::ImplicitCast(arguments[i], func.arguments[i]);
		if (cast_cost >= 0) {
			// we can implicitly cast, add the cost to the total cost
			cost += cast_cost;
		} else {
			// we can't implicitly cast: throw an error
			return -1;
		}
	}
	return cost;
}

template<class T>
static index_t BindFunctionFromArguments(string name, vector<T> &functions, vector<SQLType> &arguments) {
	index_t best_function = INVALID_INDEX;
	int64_t lowest_cost = numeric_limits<int64_t>::max();
	vector<index_t> conflicting_functions;
	for(index_t f_idx = 0; f_idx < functions.size(); f_idx++) {
		auto &func = functions[f_idx];
		// check the arguments of the function
		int64_t cost = BindFunctionCost(func, arguments);
		if (cost < 0) {
			// auto casting was not possible
			continue;
		}
		if (cost == lowest_cost) {
			conflicting_functions.push_back(f_idx);
			continue;
		}
		if (cost > lowest_cost) {
			continue;
		}
		conflicting_functions.clear();
		lowest_cost = cost;
		best_function = f_idx;
	}
	if (conflicting_functions.size() > 0) {
		// there are multiple possible function definitions
		// throw an exception explaining which overloads are there
		conflicting_functions.push_back(best_function);
		string call_str = Function::CallToString(name, arguments);
		string candidate_str = "";
		for(auto &conf : conflicting_functions) {
			auto &f = functions[conf];
			candidate_str += "\t" + f.ToString() + "\n";
		}
		throw BinderException("Could not choose a best candidate function for the function call \"%s\". In order to select one, please add explicit type casts.\n\tCandidate functions:\n%s", call_str.c_str(), candidate_str.c_str());
	}
	if (best_function == INVALID_INDEX) {
		// no matching function was found, throw an error
		string call_str = Function::CallToString(name, arguments);
		string candidate_str = "";
		for(auto &f : functions) {
			candidate_str += "\t" + f.ToString() + "\n";
		}
		throw BinderException("No function matches the given name and argument types '%s'. You might need to add explicit type casts.\n\tCandidate functions:\n%s", call_str.c_str(), candidate_str.c_str());
	}
	return best_function;
}

index_t Function::BindFunction(string name, vector<ScalarFunction> &functions, vector<SQLType> &arguments) {
	return BindFunctionFromArguments(name, functions, arguments);
}

index_t Function::BindFunction(string name, vector<AggregateFunction> &functions, vector<SQLType> &arguments)  {
	return BindFunctionFromArguments(name, functions, arguments);
}
