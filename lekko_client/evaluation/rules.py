import struct

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

    #rule_value = getattr(rule, rule_type)

    if rule_type == "bool_const":
        return rule.bool_const
    elif rule_type == "not":
        return not evaluate_rule(rule_value, namespace, config_name, context)
    elif rule_type == "logical_expression":
        expr = rule.logical_expression
        if not expr.rules:
            raise EvaluationError("No rules found in logical expression")

        logical_operator = expr.logical_operator
        return (
            all(evaluate_rule(r, namespace, config_name, context) for r in expr.rules)
            if logical_operator == LogicalOperator.LOGICAL_OPERATOR_AND
            else any(evaluate_rule(r, namespace, config_name, context) for r in expr.rules)
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
            return evaluate_number_comparator(
                atom.comparison_operator, atom.comparison_value, context_value
            )
        elif atom.comparison_operator == ComparisonOperator.COMPARISON_OPERATOR_CONTAINED_WITHIN:
            return evaluate_contained_within(atom.comparison_value, context_value)
        elif atom.comparison_operator in (
            ComparisonOperator.COMPARISON_OPERATOR_STARTS_WITH,
            ComparisonOperator.COMPARISON_OPERATOR_ENDS_WITH,
            ComparisonOperator.COMPARISON_OPERATOR_CONTAINS,
        ):
            return evaluate_string_comparator(
                atom.comparison_operator, atom.comparison_value, context_value
            )
        else:
            raise EvaluationError("Unknown comparison operator")
    elif rule_type == "call_expression":
        expr = rule.call_expression
        if expr.WhichOneof("function") == "bucket":
            return evaluate_bucket(expr.bucket, namespace, config_name, context)
        else:
            raise EvaluationError("Unknown CallExpression function type")
    else:
        raise EvaluationError("Unknown rule type")


def evaluate_equals(rule_value: Value, context_value: LekkoValue) -> bool:
    rule_kind = rule_value.WhichOneof("kind") or ""
    context_kind = context_value.WhichOneof("kind") or ""
    if rule_kind not in ["bool_value", "string_value", "number_value"]:
        raise EvaluationError("Unsupported rule type for equals operator")

    if rule_kind == "number_value":
        if context_kind not in ["double_value", "int_value"]:
            raise EvaluationError("Type mismatch in equals operator rule")
    elif rule_kind != context_kind:
        raise EvaluationError("Type mismatch in equals operator rule")

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
        raise EvaluationError("Unknown string comparison operator")


def get_string(value: Value | LekkoValue) -> str:
    if not value:
        raise EvaluationError("String Value is undefined")

    if value.WhichOneof("kind") == "string_value":
        return value.string_value
    else:
        raise EvaluationError("get_string called with non-string Value")


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
        raise EvaluationError("Unknown numerical comparison operator")


def get_number(value: Value | LekkoValue) -> float:
    value_kind = value.WhichOneof("kind")
    if value_kind in ["number_value", "int_value", "double_value"]:
        return float(getattr(value, value_kind))
    else:
        raise EvaluationError("get_number caled with non-numeric Value")


def evaluate_contained_within(rule_value: Value, context_value: LekkoValue) -> bool:
    if rule_value.WhichOneof("kind") != "list_value":
        raise EvaluationError("Contained within operator must use a list value")

    # TODO: this will throw if there's a type mismatch, which means that all items in rule list must be of same type
    # This is consistent with other language SDKs, but we should consider just returning False on type mismatch
    return any(evaluate_equals(list_elem_val, context_value) for list_elem_val in rule_value.list_value.values)


def evaluate_bucket(bucket_f: CallExpression.Bucket, namespace: str, config_name: str, context: ClientContext) -> bool:
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
        raise EvaluationError("Unsupported value type for bucket")

    bytes_frags = [bytes(namespace, "utf-8"), bytes(config_name, "utf-8"), bytes(ctx_key, "utf-8"), bytes_buffer]
    result = xxh32(b"".join(bytes_frags), 0).intdigest()
    return result % 100000 <= bucket_f.threshold
