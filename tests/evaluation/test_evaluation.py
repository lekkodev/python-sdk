from typing import List

import pytest
from google.protobuf.wrappers_pb2 import Int64Value

from lekko_client.evaluation.evaluation import evaluate
from lekko_client.evaluation.rules import ClientContext
from lekko_client.gen.lekko.feature.v1beta1.feature_pb2 import Feature
from lekko_client.helpers import convert_context


@pytest.mark.parametrize(
    "context,expected",
    [
        ({"a": 1}, 0),
        ({"a": 1, "c": 3}, 1),
        ({"c": 3}, 2),
        ({"f": 3}, 0),
        ({"f": 5}, 5),
        ({"h": 4}, 7),
        ({"i": 4}, 8),
        ({"p": "a foo bar"}, 15),
        ({"q": "hello world"}, 16),
        ({"r": "a foo bar"}, 17),
        ({"s": 2}, 18),
        ({"t": "anything"}, 19),
        ({"u": 11}, 20),
    ],
)
def test_complex_evaluation(test_complex_rule_feature, context, expected):
    client_context = convert_context(context)
    result = evaluate(test_complex_rule_feature, "default", client_context)
    inner_result = Int64Value()
    assert result.value.Unpack(inner_result)
    assert inner_result.value == expected


@pytest.mark.only
def test_empty_config_tree():
    with pytest.raises(Exception):
        evaluate(Feature(), "ns")


@pytest.mark.parametrize(
    "feature_fixture_name,test_context,expected_fixture_name,expected_path",
    [
        ("test_feature_no_constraints", convert_context({}), "test_feature_default_value", []),
        ("test_feature_no_constraints", convert_context({"key": "anything"}), "test_feature_default_value", []),
        ("test_feature_no_constraints", None, "test_feature_default_value", []),
        ("test_feature_one_level_traversal", convert_context({}), "test_feature_default_value", []),
        ("test_feature_one_level_traversal", convert_context({"age": 5}), "test_feature_default_value", []),
        ("test_feature_one_level_traversal", convert_context({"age": 10}), "test_feature_constraint_value", [0]),
        ("test_feature_one_level_traversal", convert_context({"age": 12}), "test_feature_constraint_value", [1]),
        ("test_feature_two_level_traversal", convert_context({}), "test_feature_default_value", []),
        ("test_feature_two_level_traversal", convert_context({"age": 10}), "test_feature_constraint_value", [0]),
        (
            "test_feature_two_level_traversal",
            convert_context({"age": 10, "city": "Rome"}),
            "test_feature_constraint_value",
            [0, 0],
        ),
        (
            "test_feature_two_level_traversal",
            convert_context({"age": 10, "city": "Paris"}),
            "test_feature_constraint_value",
            [0, 1],
        ),
        (
            "test_feature_two_level_traversal",
            convert_context({"age": 12, "city": "Milan"}),
            "test_feature_constraint_value",
            [1],
        ),
        ("test_feature_two_level_traversal", convert_context({"age": 12}), "test_feature_constraint_value", [1]),
        (
            "test_feature_two_level_traversal",
            convert_context({"age": 12, "city": "Rome"}),
            "test_feature_constraint_value",
            [1, 0],
        ),
        (
            "test_feature_two_level_traversal",
            convert_context({"age": 12, "city": "Paris"}),
            "test_feature_constraint_value",
            [1, 1],
        ),
        (
            "test_feature_two_level_traversal",
            convert_context({"age": 12, "city": "Milan"}),
            "test_feature_constraint_value",
            [1],
        ),
    ],
)
def test_eval(
    feature_fixture_name: str,
    test_context: ClientContext,
    expected_fixture_name: str,
    expected_path: List[int],
    request,
):
    test_feature = request.getfixturevalue(feature_fixture_name)
    expected = request.getfixturevalue(expected_fixture_name)
    if expected is not None:
        result = evaluate(test_feature, "ns_1", test_context)
        assert result.value == expected
        assert result.path == expected_path
    else:
        assert not "test case needs to either expect an error or a result"
