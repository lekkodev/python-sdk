from typing import Any

import pytest
from google.protobuf.struct_pb2 import Struct, Value

from lekko_client.evaluation.rules import evaluate_rule
from lekko_client.gen.lekko.rules.v1beta3.rules_pb2 import (
    Atom,
    CallExpression,
    ComparisonOperator,
    LogicalExpression,
    LogicalOperator,
    Rule,
)
from lekko_client.helpers import convert_context


@pytest.mark.parametrize(
    "context_val,namespace,config_name,expected",
    [
        (1, "ns_1", "feature_1", False),
        (2, "ns_1", "feature_1", False),
        (3, "ns_1", "feature_1", True),
        (4, "ns_1", "feature_1", False),
        (5, "ns_1", "feature_1", True),
        (101, "ns_1", "feature_1", True),
        (102, "ns_1", "feature_1", True),
        (103, "ns_1", "feature_1", False),
        (104, "ns_1", "feature_1", False),
        (105, "ns_1", "feature_1", True),
        (1, "ns_2", "feature_2", False),
        (2, "ns_2", "feature_2", True),
        (3, "ns_2", "feature_2", False),
        (4, "ns_2", "feature_2", False),
        (5, "ns_2", "feature_2", True),
        (101, "ns_2", "feature_2", True),
        (102, "ns_2", "feature_2", True),
        (103, "ns_2", "feature_2", False),
        (104, "ns_2", "feature_2", True),
        (105, "ns_2", "feature_2", True),
        (3.1415, "ns_1", "feature_1", False),
        (2.7182, "ns_1", "feature_1", False),
        (1.6180, "ns_1", "feature_1", True),
        (6.6261, "ns_1", "feature_1", True),
        (6.0221, "ns_1", "feature_1", False),
        (2.9979, "ns_1", "feature_1", True),
        (6.6730, "ns_1", "feature_1", False),
        (1.3807, "ns_1", "feature_1", True),
        (1.4142, "ns_1", "feature_1", True),
        (2.0000, "ns_1", "feature_1", False),
        (3.1415, "ns_2", "feature_2", True),
        (2.7182, "ns_2", "feature_2", False),
        (1.6180, "ns_2", "feature_2", True),
        (6.6261, "ns_2", "feature_2", False),
        (6.0221, "ns_2", "feature_2", False),
        (2.9979, "ns_2", "feature_2", False),
        (6.6730, "ns_2", "feature_2", False),
        (1.3807, "ns_2", "feature_2", False),
        (1.4142, "ns_2", "feature_2", True),
        (2.0000, "ns_2", "feature_2", False),
        ("hello", "ns_1", "feature_1", False),
        ("world", "ns_1", "feature_1", False),
        ("i", "ns_1", "feature_1", True),
        ("am", "ns_1", "feature_1", True),
        ("a", "ns_1", "feature_1", True),
        ("unit", "ns_1", "feature_1", False),
        ("test", "ns_1", "feature_1", True),
        ("case", "ns_1", "feature_1", True),
        ("for", "ns_1", "feature_1", False),
        ("bucket", "ns_1", "feature_1", False),
        ("hello", "ns_2", "feature_2", True),
        ("world", "ns_2", "feature_2", False),
        ("i", "ns_2", "feature_2", True),
        ("am", "ns_2", "feature_2", True),
        ("a", "ns_2", "feature_2", True),
        ("unit", "ns_2", "feature_2", False),
        ("test", "ns_2", "feature_2", True),
        ("case", "ns_2", "feature_2", False),
        ("for", "ns_2", "feature_2", False),
        ("bucket", "ns_2", "feature_2", False),
    ],
)
def test_bucket(context_val, namespace, config_name, expected):
    rule = Rule(call_expression=CallExpression(bucket=CallExpression.Bucket(context_key="key", threshold=50000)))
    context = convert_context({"key": context_val})
    assert evaluate_rule(rule, namespace, config_name, context) == expected


def test_bool_const():
    for b in [True, False]:
        rule = Rule(bool_const=b)
        assert evaluate_rule(rule, "ns1", "config1") == b


def test_present():
    rule = Rule(atom=Atom(context_key="age", comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_PRESENT))
    assert evaluate_rule(rule, "ns1", "config1") is False
    assert evaluate_rule(rule, "ns1", "config1", convert_context({"age": 10})) is True
    assert evaluate_rule(rule, "ns1", "config1", convert_context({"age": "not a number"})) is True


def convert_to_value(v: Any) -> Value:
    s = Struct()
    s.update({"key": v})
    return s.fields["key"]


@pytest.mark.parametrize(
    "test_atom,test_context,expected,raises",
    [
        (
            Atom(
                context_key="isprod",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                comparison_value=convert_to_value(True),
            ),
            convert_context({"isprod": True}),
            True,
            False,
        ),
        (
            Atom(
                context_key="isprod",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                comparison_value=convert_to_value(True),
            ),
            convert_context({"isprod": False}),
            False,
            False,
        ),
        (
            Atom(
                context_key="isprod",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                comparison_value=convert_to_value(True),
            ),
            convert_context({"isprod": "not a bool"}),
            False,
            True,
        ),
        (
            Atom(
                context_key="age",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                comparison_value=convert_to_value(12),
            ),
            convert_context({"age": 12}),
            True,
            False,
        ),
        (
            Atom(
                context_key="age",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                comparison_value=convert_to_value(12),
            ),
            convert_context({"age": 35}),
            False,
            False,
        ),
        (
            Atom(
                context_key="age",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                comparison_value=convert_to_value(12),
            ),
            convert_context({"age": 12.001}),
            False,
            False,
        ),
        (
            Atom(
                context_key="age",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                comparison_value=convert_to_value(12.001),
            ),
            convert_context({"age": 12.001}),
            True,
            False,
        ),
        (
            Atom(
                context_key="age",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                comparison_value=convert_to_value(12),
            ),
            convert_context({"age": "not a number"}),
            False,
            True,
        ),
        (
            Atom(
                context_key="age",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_NOT_EQUALS,
                comparison_value=convert_to_value(12),
            ),
            convert_context({"age": 25}),
            True,
            False,
        ),
        (
            Atom(
                context_key="age",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_NOT_EQUALS,
                comparison_value=convert_to_value(12),
            ),
            convert_context({"age": 12}),
            False,
            False,
        ),
        (
            Atom(
                context_key="age",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                comparison_value=convert_to_value(12),
            ),
            convert_context({}),  # not present
            False,
            False,
        ),
        (
            Atom(
                context_key="city",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                comparison_value=convert_to_value("Rome"),
            ),
            convert_context({"city": "Rome"}),
            True,
            False,
        ),
        (
            Atom(
                context_key="city",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                comparison_value=convert_to_value("Rome"),
            ),
            convert_context({"city": "rome"}),
            False,
            False,
        ),
        (
            Atom(
                context_key="city",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                comparison_value=convert_to_value("Rome"),
            ),
            convert_context({"city": "Paris"}),
            False,
            False,
        ),
        (
            Atom(
                context_key="city",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                comparison_value=convert_to_value("Rome"),
            ),
            convert_context({"city": 99}),
            False,
            True,
        ),
        (
            Atom(
                context_key="age",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN,
                comparison_value=convert_to_value(12),
            ),
            convert_context({"age": 12}),
            False,
            False,
        ),
        (
            Atom(
                context_key="age",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN,
                comparison_value=convert_to_value(12),
            ),
            convert_context({"age": 11}),
            True,
            False,
        ),
        (
            Atom(
                context_key="age",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN_OR_EQUALS,
                comparison_value=convert_to_value(12),
            ),
            convert_context({"age": 12}),
            True,
            False,
        ),
        (
            Atom(
                context_key="age",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_GREATER_THAN_OR_EQUALS,
                comparison_value=convert_to_value(12),
            ),
            convert_context({"age": 12}),
            True,
            False,
        ),
        (
            Atom(
                context_key="age",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_GREATER_THAN,
                comparison_value=convert_to_value(12),
            ),
            convert_context({"age": 12}),
            False,
            False,
        ),
        (
            Atom(
                context_key="age",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_GREATER_THAN,
                comparison_value=convert_to_value(12),
            ),
            convert_context({"age": 13}),
            True,
            False,
        ),
        (
            Atom(
                context_key="age",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_GREATER_THAN,
                comparison_value=convert_to_value(12),
            ),
            convert_context({"age": "not a number"}),
            False,
            True,
        ),
        (
            Atom(
                context_key="city",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_CONTAINED_WITHIN,
                comparison_value=convert_to_value(["Rome", "Paris"]),
            ),
            convert_context({"city": "London"}),
            False,
            False,
        ),
        (
            Atom(
                context_key="city",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_CONTAINED_WITHIN,
                comparison_value=convert_to_value(["Rome", "Paris"]),
            ),
            convert_context({"city": "Rome"}),
            True,
            False,
        ),
        (
            Atom(
                context_key="city",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_CONTAINED_WITHIN,
                comparison_value=convert_to_value(["Rome", "Paris"]),
            ),
            convert_context({}),  # not present
            False,
            False,
        ),
        (
            Atom(
                context_key="city",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_CONTAINED_WITHIN,
                comparison_value=convert_to_value(["Rome", "Paris"]),
            ),
            convert_context({"city": "rome"}),
            False,
            False,
        ),
        (
            Atom(
                context_key="city",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_STARTS_WITH,
                comparison_value=convert_to_value("Ro"),
            ),
            convert_context({"city": "Rome"}),
            True,
            False,
        ),
        (
            Atom(
                context_key="city",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_STARTS_WITH,
                comparison_value=convert_to_value("Ro"),
            ),
            convert_context({"city": "London"}),
            False,
            False,
        ),
        (
            Atom(
                context_key="city",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_STARTS_WITH,
                comparison_value=convert_to_value("Ro"),
            ),
            convert_context({"city": "rome"}),
            False,
            False,
        ),
        (
            Atom(
                context_key="city",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_STARTS_WITH,
                comparison_value=convert_to_value("Ro"),
            ),
            None,  # not present
            False,
            False,
        ),
        (
            Atom(
                context_key="city",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_ENDS_WITH,
                comparison_value=convert_to_value("me"),
            ),
            convert_context({"city": "Rome"}),
            True,
            False,
        ),
        (
            Atom(
                context_key="city",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_ENDS_WITH,
                comparison_value=convert_to_value("me"),
            ),
            convert_context({"city": "London"}),
            False,
            False,
        ),
        (
            Atom(
                context_key="city",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_CONTAINS,
                comparison_value=convert_to_value(""),
            ),
            convert_context({"city": "Rome"}),
            True,
            False,
        ),
        (
            Atom(
                context_key="city",
                comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_CONTAINS,
                comparison_value=convert_to_value("foo"),
            ),
            convert_context({"city": "Rome"}),
            False,
            False,
        ),
    ],
)
def test_atom(test_atom, test_context, expected, raises):
    rule = Rule(atom=test_atom)
    if raises:
        with pytest.raises(Exception):
            evaluate_rule(rule, "ns1", "config1", test_context)
    else:
        assert evaluate_rule(rule, "ns1", "config1", test_context) == expected


@pytest.mark.parametrize(
    "test_atoms,logical_op,test_context,expected,raises",
    [
        (
            [
                Atom(
                    context_key="age",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN,
                    comparison_value=convert_to_value(5),
                ),
                Atom(
                    context_key="age",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_GREATER_THAN,
                    comparison_value=convert_to_value(10),
                ),
            ],
            LogicalOperator.LOGICAL_OPERATOR_OR,
            convert_context({"age": 8}),
            False,
            False,
        ),
        (
            [
                Atom(
                    context_key="age",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN,
                    comparison_value=convert_to_value(5),
                ),
                Atom(
                    context_key="age",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_GREATER_THAN,
                    comparison_value=convert_to_value(10),
                ),
            ],
            LogicalOperator.LOGICAL_OPERATOR_OR,
            convert_context({"age": 12}),
            True,
            False,
        ),
        (
            [
                Atom(
                    context_key="age",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN,
                    comparison_value=convert_to_value(5),
                ),
                Atom(
                    context_key="city",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                    comparison_value=convert_to_value("Rome"),
                ),
            ],
            LogicalOperator.LOGICAL_OPERATOR_AND,
            convert_context({"age": 8, "city": "Rome"}),
            False,
            False,
        ),
        (
            [
                Atom(
                    context_key="age",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN,
                    comparison_value=convert_to_value(5),
                ),
                Atom(
                    context_key="city",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                    comparison_value=convert_to_value("Rome"),
                ),
            ],
            LogicalOperator.LOGICAL_OPERATOR_AND,
            convert_context({"age": 3, "city": "Rome"}),
            True,
            False,
        ),
        (
            [
                Atom(
                    context_key="age",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN,
                    comparison_value=convert_to_value(5),
                ),
                Atom(
                    context_key="city",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                    comparison_value=convert_to_value("Rome"),
                ),
            ],
            LogicalOperator.LOGICAL_OPERATOR_UNSPECIFIED,
            convert_context({"age": 3}),
            True,
            False,
        ),
        (
            [
                Atom(
                    context_key="age",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN,
                    comparison_value=convert_to_value(5),
                ),
                Atom(
                    context_key="city",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                    comparison_value=convert_to_value("Rome"),
                ),
            ],
            LogicalOperator.LOGICAL_OPERATOR_AND,
            convert_context({"age": 3}),
            False,
            False,
        ),
        (
            [
                Atom(
                    context_key="age",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN,
                    comparison_value=convert_to_value(5),
                )
            ],
            LogicalOperator.LOGICAL_OPERATOR_AND,
            convert_context({"age": 3}),
            True,
            False,
        ),
        (
            [
                Atom(
                    context_key="age",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN,
                    comparison_value=convert_to_value(5),
                )
            ],
            LogicalOperator.LOGICAL_OPERATOR_OR,
            convert_context({"age": 3}),
            True,
            False,
        ),
        ([], LogicalOperator.LOGICAL_OPERATOR_AND, convert_context({}), False, True),
        (
            [
                Atom(
                    context_key="age",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN,
                    comparison_value=convert_to_value(5),
                ),
                Atom(
                    context_key="city",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                    comparison_value=convert_to_value("Rome"),
                ),
                Atom(
                    context_key="age",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                    comparison_value=convert_to_value(8),
                ),
            ],
            LogicalOperator.LOGICAL_OPERATOR_AND,
            convert_context({"age": 8}),
            False,
            False,
        ),
        (
            [
                Atom(
                    context_key="age",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_LESS_THAN,
                    comparison_value=convert_to_value(5),
                ),
                Atom(
                    context_key="city",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                    comparison_value=convert_to_value("Rome"),
                ),
                Atom(
                    context_key="age",
                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                    comparison_value=convert_to_value(8),
                ),
            ],
            LogicalOperator.LOGICAL_OPERATOR_OR,
            convert_context({"age": 8}),
            True,
            False,
        ),
    ],
)
def test_logical_op(test_atoms, logical_op, test_context, expected, raises):
    rule = Rule(
        logical_expression=LogicalExpression(
            rules=[Rule(atom=atom) for atom in test_atoms], logical_operator=logical_op
        )
    )

    if raises:
        with pytest.raises(Exception):
            evaluate_rule(rule, "ns_1", "feature_1", test_context)
    else:
        assert evaluate_rule(rule, "ns_1", "feature_1", test_context) == expected
