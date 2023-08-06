//===----------------------------------------------------------------------===//
//                         DuckDB
//
// parser/tokens.hpp
//
//
//===----------------------------------------------------------------------===//

#pragma once

namespace duckdb {

//===--------------------------------------------------------------------===//
// Statements
//===--------------------------------------------------------------------===//
class SQLStatement;

class AlterTableStatement;
class CopyStatement;
class CreateIndexStatement;
class CreateSchemaStatement;
class CreateTableStatement;
class CreateViewStatement;
class DeleteStatement;
class DropStatement;
class InsertStatement;
class SelectStatement;
class TransactionStatement;
class UpdateStatement;
class PrepareStatement;
class ExecuteStatement;
class DeallocateStatement;
class CreateSequenceStatement;

//===--------------------------------------------------------------------===//
// Query Node
//===--------------------------------------------------------------------===//
class QueryNode;
class SelectNode;
class SetOperationNode;

//===--------------------------------------------------------------------===//
// Expressions
//===--------------------------------------------------------------------===//
class ParsedExpression;

class CaseExpression;
class CastExpression;
class ColumnRefExpression;
class ComparisonExpression;
class ConjunctionExpression;
class ConstantExpression;
class DefaultExpression;
class FunctionExpression;
class OperatorExpression;
class ParameterExpression;
class StarExpression;
class SubqueryExpression;
class WindowExpression;

//===--------------------------------------------------------------------===//
// Constraints
//===--------------------------------------------------------------------===//
class Constraint;

class NotNullConstraint;
class CheckConstraint;
class UniqueConstraint;

//===--------------------------------------------------------------------===//
// TableRefs
//===--------------------------------------------------------------------===//
class TableRef;

class BaseTableRef;
class CrossProductRef;
class JoinRef;
class SubqueryRef;
class TableFunctionRef;

} // namespace duckdb
