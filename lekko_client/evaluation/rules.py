import struct
from typing import assert_never

from google.protobuf.struct_pb2 import Value
from xxhash import xxh32

from lekko_client.exceptions import EvaluationError
from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2 import (
    Value as LekkoValue,
)
from lekko_client.gen.lekko.rules.v1beta3.rules_pb2 import (
    CallExpression,
    ComparisonOperator,
    LogicalOperator,
    Rule,
)
from lekko_client.models import ClientContext


def evaluate_rule(rule: Rule, namespace: str, config_name: str, context: ClientContext = None) -> bool:
    if not rule:
        raise EvaluationError("Empty rule")

    rule_type = rule.WhichOneof("rule")
    if not rule_type:
        raise EvaluationError("Empty rule")

    if rule_type == "bool_const":
        return rule.bool_const
    elif rule_type == "not":
        # have to use `getattr` because `not` is a reserved keyword
        rule_value = getattr(rule, rule_type)
        return not evaluate_rule(rule_value, namespace, config_name, context)
    elif rule_type == "logical_expression":
        logical_expression = rule.logical_expression
        if not logical_expression.rules:
            raise EvaluationError("No rules found in logical expression")

        logical_operator = logical_expression.logical_operator
        return (
            all(evaluate_rule(r, namespace, config_name, context) for r in logical_expression.rules)
            if logical_operator == LogicalOperator.LOGICAL_OPERATOR_AND
            else any(evaluate_rule(r, namespace, config_name, context) for r in logical_expression.rules)
        )
    elif rule_type == "atom":
        atom = rule.atom
        context_key = atom.context_key
        context_value = context.get(context_key) if context else None

        if atom.comparison_operator == ComparisonOperator.COMPARISON_OPERATOR_PRESENT:
            return context_value is not None

        if context_value is None:
            return False

        if atom.comparison_operator == ComparisonOperator.COMPARISON_OPERATOR_EQUALS:
            return evaluate_equals(atom.comparison_value, context_value)
        elif atom.comparison_operator == ComparisonOperator.COMPARISON_OPERATOR_NOT_EQUALS:
            return not evaluate_equals(atom.comparison_value, context_value)
        elif atom.comparison_operator in (
            ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN,
            ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN_OR_EQUALS,
            ComparisonOperator.COMPARISON_OPERATOR_GREATER_THAN,
            ComparisonOperator.COMPARISON_OPERATOR_GREATER_THAN_OR_EQUALS,
        ):
            return evaluate_number_comparator(atom.comparison_operator, atom.comparison_value, context_value)
        elif atom.comparison_operator == ComparisonOperator.COMPARISON_OPERATOR_CONTAINED_WITHIN:
            return evaluate_contained_within(atom.comparison_value, context_value)
        elif atom.comparison_operator in (
            ComparisonOperator.COMPARISON_OPERATOR_STARTS_WITH,
            ComparisonOperator.COMPARISON_OPERATOR_ENDS_WITH,
            ComparisonOperator.COMPARISON_OPERATOR_CONTAINS,
        ):
            return evaluate_string_comparator(atom.comparison_operator, atom.comparison_value, context_value)
        else:
            raise EvaluationError("Unknown comparison operator")
    elif rule_type == "call_expression":
        call_expression = rule.call_expression
        fn_type = call_expression.WhichOneof("function")
        if fn_type is None:
            raise EvaluationError("Empty call expression")
        if fn_type == "bucket":
            return evaluate_bucket(call_expression.bucket, namespace, config_name, context)
        else:
            assert_never(fn_type)
    else:
        assert_never(rule_type)


def evaluate_equals(rule_value: Value, context_value: LekkoValue) -> bool:
    rule_kind = rule_value.WhichOneof("kind")
    if rule_kind not in ["bool_value", "string_value", "number_value"]:
        raise EvaluationError("Unsupported rule type for equals operator")

    context_kind = context_value.WhichOneof("kind")

    if context_kind == rule_kind == "string_value":
        return rule_value.string_value == context_value.string_value
    if context_kind == rule_kind == "bool_value":
        return rule_value.bool_value == context_value.bool_value
    if rule_kind == "number_value":
        if context_kind == "double_value":
            return rule_value.number_value == context_value.double_value
        if context_kind == "int_value":
            return rule_value.number_value == context_value.int_value
    raise EvaluationError(f"Type mismatch in equals operator rule: {rule_kind} and {context_kind}")


def evaluate_string_comparator(
    comparison_operator: ComparisonOperator.ValueType,
    rule_value: Value,
    context_value: LekkoValue,
) -> bool:
    rule_str = get_string(rule_value)
    context_str = get_string(context_value)

    if comparison_operator == ComparisonOperator.COMPARISON_OPERATOR_STARTS_WITH:
        return context_str.startswith(rule_str)
    elif comparison_operator == ComparisonOperator.COMPARISON_OPERATOR_ENDS_WITH:
        return context_str.endswith(rule_str)
    elif comparison_operator == ComparisonOperator.COMPARISON_OPERATOR_CONTAINS:
        return rule_str in context_str
    else:
        raise EvaluationError("Unknown string comparison operator")


def get_string(value: Value | LekkoValue) -> str:
    if not value:
        raise EvaluationError("String Value is undefined")

    if value.WhichOneof("kind") == "string_value":
        return value.string_value
    else:
        raise EvaluationError("get_string called with non-string Value")


def evaluate_number_comparator(
    comparison_operator: ComparisonOperator.ValueType,
    rule_value: Value,
    context_value: LekkoValue,
) -> bool:
    rule_num = get_number(rule_value)
    context_num = get_number(context_value)

    if comparison_operator == ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN:
        return context_num < rule_num
    elif comparison_operator == ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN_OR_EQUALS:
        return context_num <= rule_num
    elif comparison_operator == ComparisonOperator.COMPARISON_OPERATOR_GREATER_THAN:
        return context_num > rule_num
    elif comparison_operator == ComparisonOperator.COMPARISON_OPERATOR_GREATER_THAN_OR_EQUALS:
        return context_num >= rule_num
    else:
        raise EvaluationError("Unknown numerical comparison operator")


def get_number(value: Value | LekkoValue) -> float:
    match [value, value.WhichOneof("kind")]:
        case [LekkoValue() as lekko_value, "double_value"]:
            return float(lekko_value.double_value)
        case [LekkoValue() as lekko_value, "int_value"]:
            return float(lekko_value.int_value)
        case [Value() as json_value, "number_value"]:
            return float(json_value.number_value)
    raise EvaluationError("get_number caled with non-numeric Value")


def evaluate_contained_within(rule_value: Value, context_value: LekkoValue) -> bool:
    if rule_value.WhichOneof("kind") != "list_value":
        raise EvaluationError("Contained within operator must use a list value")

    # TODO: this will throw if there's a type mismatch, which means that all items in rule list must be of same type
    # This is consistent with other language SDKs, but we should consider just returning False on type mismatch
    return any(evaluate_equals(list_elem_val, context_value) for list_elem_val in rule_value.list_value.values)


def evaluate_bucket(
    bucket_f: CallExpression.Bucket,
    namespace: str,
    config_name: str,
    context: ClientContext,
) -> bool:
    ctx_key = bucket_f.context_key
    value = context.get(ctx_key) if context else None
    if not value:
        # If key is missing in context map, evaluate to false - move to next rule
        return False

    bytes_buffer: bytes = b""

    value_kind = value.WhichOneof("kind")
    if not value_kind:
        return False

    if value_kind == "string_value":
        bytes_buffer = bytes(value.string_value, "utf-8")
    elif value_kind == "int_value":
        bytes_buffer = value.int_value.to_bytes(8, byteorder="big")
    elif value_kind == "double_value":
        bytes_buffer = struct.pack(">d", value.double_value)
    else:
        raise EvaluationError("Unsupported value type for bucket")

    bytes_frags = [
        bytes(namespace, "utf-8"),
        bytes(config_name, "utf-8"),
        bytes(ctx_key, "utf-8"),
        bytes_buffer,
    ]
    result = xxh32(b"".join(bytes_frags), 0).intdigest()
    return result % 100000 <= bucket_f.threshold
