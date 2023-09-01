import struct
from typing import Dict, Optional, Union

from google.protobuf.struct_pb2 import Value
from xxhash import xxh32

from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2 import (
    Value as LekkoValue,
)
from lekko_client.gen.lekko.rules.v1beta3.rules_pb2 import (
    CallExpression,
    ComparisonOperator,
    LogicalOperator,
    Rule,
)

ClientContext = Optional[Dict[str, LekkoValue]]


def evaluate_rule(rule: Rule, namespace: str, config_name: str, context: ClientContext = None) -> bool:
    if not rule:
        raise ValueError("empty rule")

    rule_type = rule.WhichOneof("rule")
    if not rule_type:
        raise ValueError("empty rule")

    rule_value = getattr(rule, rule_type)

    if rule_type == "bool_const":
        return rule_value
    elif rule_type == "not":
        return not evaluate_rule(rule_value, namespace, config_name, context)
    elif rule_type == "logical_expression":
        if not rule_value.rules:
            raise ValueError("no rules found in logical expression")

        logical_operator = rule_value.logical_operator
        return (
            all(evaluate_rule(r, namespace, config_name, context) for r in rule_value.rules)
            if logical_operator == LogicalOperator.LOGICAL_OPERATOR_AND
            else any(evaluate_rule(r, namespace, config_name, context) for r in rule_value.rules)
        )
    elif rule_type == "atom":
        context_key = rule_value.context_key
        context_value = context.get(context_key) if context else None

        if rule_value.comparison_operator == ComparisonOperator.COMPARISON_OPERATOR_PRESENT:
            return context_value is not None

        if context_value is None:
            return False

        if rule_value.comparison_operator == ComparisonOperator.COMPARISON_OPERATOR_EQUALS:
            return evaluate_equals(rule_value.comparison_value, context_value)
        elif rule_value.comparison_operator == ComparisonOperator.COMPARISON_OPERATOR_NOT_EQUALS:
            return not evaluate_equals(rule_value.comparison_value, context_value)
        elif rule_value.comparison_operator in (
            ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN,
            ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN_OR_EQUALS,
            ComparisonOperator.COMPARISON_OPERATOR_GREATER_THAN,
            ComparisonOperator.COMPARISON_OPERATOR_GREATER_THAN_OR_EQUALS,
        ):
            return evaluate_number_comparator(
                rule_value.comparison_operator, rule_value.comparison_value, context_value
            )
        elif rule_value.comparison_operator == ComparisonOperator.COMPARISON_OPERATOR_CONTAINED_WITHIN:
            return evaluate_contained_within(rule_value.comparison_value, context_value)
        elif rule_value.comparison_operator in (
            ComparisonOperator.COMPARISON_OPERATOR_STARTS_WITH,
            ComparisonOperator.COMPARISON_OPERATOR_ENDS_WITH,
            ComparisonOperator.COMPARISON_OPERATOR_CONTAINS,
        ):
            return evaluate_string_comparator(
                rule_value.comparison_operator, rule_value.comparison_value, context_value
            )
        else:
            raise ValueError("unknown comparison operator")
    elif rule_type == "call_expression":
        if rule_value.WhichOneof("function") == "bucket":
            return evaluate_bucket(rule_value.bucket, namespace, config_name, context)
        else:
            raise ValueError("unknown function type")
    else:
        raise ValueError("unknown rule type")


def evaluate_equals(rule_value: Value, context_value: LekkoValue) -> bool:
    rule_kind = rule_value.WhichOneof("kind") or ""
    context_kind = context_value.WhichOneof("kind") or ""
    if rule_kind not in ["bool_value", "string_value", "number_value"]:
        raise ValueError("unsupported type for equals operator")

    if rule_kind == "number_value":
        if context_kind not in ["double_value", "int_value"]:
            raise ValueError("type mismatch")
    elif rule_kind != context_kind:
        raise ValueError("type mismatch")

    return getattr(rule_value, rule_kind) == getattr(context_value, context_kind)


def evaluate_string_comparator(
    comparison_operator: ComparisonOperator, rule_value: Value, context_value: LekkoValue
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
        raise ValueError("unexpected string comparison operator")


def get_string(value: Union[Value, LekkoValue]) -> str:
    if not value:
        raise ValueError("value is undefined")

    if value.WhichOneof("kind") == "string_value":
        return value.string_value
    else:
        raise ValueError("value is not a string")


def evaluate_number_comparator(
    comparison_operator: ComparisonOperator, rule_value: Value, context_value: LekkoValue
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
        raise ValueError("unexpected numerical comparison operator")


def get_number(value: Union[Value, LekkoValue]) -> float:
    value_kind = value.WhichOneof("kind")
    if value_kind in ["number_value", "int_value", "double_value"]:
        return float(getattr(value, value_kind))
    else:
        raise ValueError("value is not a number")


def evaluate_contained_within(rule_value: Value, context_value: LekkoValue) -> bool:
    if rule_value.WhichOneof("kind") != "list_value":
        raise ValueError("type mismatch: expecting list for operator contained within")

    # TODO: this will throw if there's a type mismatch, which means that all items in rule list must be of same type
    # This is consistent with other language SDKs, but we should consider just returning False on type mismatch
    return any(evaluate_equals(list_elem_val, context_value) for list_elem_val in rule_value.list_value.values)


def evaluate_bucket(bucket_f: CallExpression.Bucket, namespace: str, config_name: str, context: ClientContext):
    ctx_key = bucket_f.context_key
    value = context.get(ctx_key) if context else None
    if not value:
        # If key is missing in context map, evaluate to false - move to next rule
        return False

    bytes_buffer: bytes = b""

    value_kind = value.WhichOneof("kind")
    if not value_kind:
        return False

    value_val = getattr(value, value_kind)
    if value_kind == "string_value":
        bytes_buffer = bytes(value_val, "utf-8")
    elif value_kind == "int_value":
        bytes_buffer = value_val.to_bytes(8, byteorder="big")
    elif value_kind == "double_value":
        bytes_buffer = struct.pack(">d", value_val)
    else:
        raise ValueError("unsupported value type for bucket")

    bytes_frags = [bytes(namespace, "utf-8"), bytes(config_name, "utf-8"), bytes(ctx_key, "utf-8"), bytes_buffer]
    result = xxh32(b"".join(bytes_frags), 0).intdigest()
    return result % 100000 <= bucket_f.threshold
