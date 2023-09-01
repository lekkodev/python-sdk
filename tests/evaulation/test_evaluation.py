import pytest
from google.protobuf.wrappers_pb2 import Int64Value

from lekko_client.evaluation.evaluation import evaluate
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
def test_evaluation(test_complex_rule_feature, context, expected):
    client_context = convert_context(context)
    result = evaluate(test_complex_rule_feature, "default", client_context)
    inner_result = Int64Value()
    assert result.value.Unpack(inner_result)
    assert inner_result.value == expected
