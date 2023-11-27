from unittest import mock

import pytest
from google.protobuf import wrappers_pb2
from google.protobuf.any_pb2 import Any as ProtoAny
from google.protobuf.message import Message as ProtoMessage
from google.protobuf.struct_pb2 import Struct

from lekko_client.clients.config_client import AnyProto
from lekko_client.clients.distribution_client import CachedDistributionClient
from lekko_client.evaluation.evaluation import EvaluationResult
from lekko_client.gen.lekko.backend.v1beta1.distribution_service_pb2 import (
    FlagEvaluationEvent,
    RepositoryKey,
)
from lekko_client.gen.lekko.feature.v1beta1.feature_pb2 import Feature
from lekko_client.helpers import convert_context, get_context_keys
from lekko_client.models import ConfigData


@pytest.mark.parametrize(
    "fn_under_test,expected",
    [
        ("get_bool", wrappers_pb2.BoolValue(value=True)),
        ("get_int", wrappers_pb2.Int64Value(value=10)),
        ("get_float", wrappers_pb2.FloatValue(value=2.5)),
        ("get_string", wrappers_pb2.StringValue(value="test_value")),
    ],
)
def test_scalar(
    mock_distribution_client: CachedDistributionClient,
    test_feature_no_constraints: Feature,
    fn_under_test: str,
    expected: ProtoMessage,
):
    mock_distribution_client.store.get.return_value = ConfigData("test_sha", test_feature_no_constraints)

    expected_any = ProtoAny()
    expected_any.Pack(expected)
    namespace = "test_namespace"
    key = test_feature_no_constraints.key
    ctx = {"ctx_key": "ctx_val"}
    with mock.patch(
        "lekko_client.clients.distribution_client.evaluate", return_value=EvaluationResult(value=expected_any, path=[1])
    ) as mock_eval:
        getattr(mock_distribution_client, fn_under_test)(namespace, key, ctx)
        res_unpacked = type(expected)()
        assert expected_any.Unpack(res_unpacked)
        assert res_unpacked == expected

        mock_eval.assert_called_once_with(test_feature_no_constraints, namespace, convert_context(ctx))
        mock_distribution_client.store.get.assert_called_once_with(namespace, key)

        # Not worth freezing time to use assert_called_once_with
        (flag_evaluation,) = mock_distribution_client.events_batcher.add_event.call_args_list[0].args
        assert flag_evaluation.repo_key == RepositoryKey(owner_name="owner", repo_name="repo")
        assert flag_evaluation.commit_sha == "test_commit_sha"
        assert flag_evaluation.feature_sha == "test_sha"
        assert flag_evaluation.namespace_name == namespace
        assert flag_evaluation.feature_name == key
        assert flag_evaluation.context_keys == get_context_keys(convert_context(ctx))
        assert flag_evaluation.result_path == [1]


@pytest.mark.parametrize(
    "expected",
    [
        [1, 2, 3],
        {"test": "dict"},
        "str",
        1.2,
        True,
    ],
)
def test_get_json(mock_distribution_client, test_feature_no_constraints, expected):
    s = Struct()
    s.update({"key": expected})
    expected_value = s.fields["key"]
    any_proto = AnyProto()
    any_proto.Pack(expected_value)

    mock_distribution_client.store.get.return_value = ConfigData("test_sha", test_feature_no_constraints)

    with mock.patch(
        "lekko_client.clients.distribution_client.evaluate", return_value=EvaluationResult(value=any_proto, path=[1])
    ):
        assert expected == mock_distribution_client.get_json("namespace", "key", {})


def test_get_proto_by_type(mock_distribution_client, test_feature_no_constraints):
    any_proto = AnyProto()
    int_proto = wrappers_pb2.Int32Value(value=10)
    any_proto.Pack(int_proto)
    mock_distribution_client.store.get.return_value = ConfigData("test_sha", test_feature_no_constraints)

    with mock.patch(
        "lekko_client.clients.distribution_client.evaluate", return_value=EvaluationResult(value=any_proto, path=[1])
    ):
        assert int_proto == mock_distribution_client.get_proto_by_type("namespace", "key", {}, wrappers_pb2.Int32Value)


def test_get_proto(mock_distribution_client, test_feature_no_constraints):
    any_proto = AnyProto()
    int_proto = wrappers_pb2.Int32Value(value=10)
    any_proto.Pack(int_proto)
    mock_distribution_client.store.get.return_value = ConfigData("test_sha", test_feature_no_constraints)

    with mock.patch(
        "lekko_client.clients.distribution_client.evaluate", return_value=EvaluationResult(value=any_proto, path=[1])
    ):
        assert int_proto == mock_distribution_client.get_proto("namespace", "key", {})

        with mock.patch("google.protobuf.symbol_database.SymbolDatabase.GetSymbol", side_effect=KeyError):
            assert any_proto == mock_distribution_client.get_proto("namespace", "key", {})


# TODO: Improve these tests - transition to more comprehensive black box test cases
def test_add_event_sample_nopass(mock_distribution_client):
    events_batcher = CachedDistributionClient.EventsBatcher(mock_distribution_client, "", 0, 0)
    for _ in range(10000):
        events_batcher.add_event(FlagEvaluationEvent())

    assert events_batcher.queue.qsize() == 10000
    # Mock random to simulate sample rate of 0
    with mock.patch("random.random", return_value=1):
        events_batcher.add_event(FlagEvaluationEvent())
        assert events_batcher.queue.qsize() == 10000


def test_add_event_sample_pass(mock_distribution_client):
    events_batcher = CachedDistributionClient.EventsBatcher(mock_distribution_client, "", 0, 0)
    for _ in range(10000):
        events_batcher.add_event(FlagEvaluationEvent())

    assert events_batcher.queue.qsize() == 10000
    # Mock random to simulate sample rate of 1
    with mock.patch("random.random", return_value=0):
        events_batcher.add_event(FlagEvaluationEvent())
        assert events_batcher.queue.qsize() == 10001


def test_accept_event(mock_distribution_client):
    events_batcher = CachedDistributionClient.EventsBatcher(mock_distribution_client, "", 0, 0)
    events_batcher.add_event(FlagEvaluationEvent())
    events_batcher._accept_event()
    assert len(events_batcher.events) == 1


def test_accept_event_sentinel(mock_distribution_client):
    events_batcher = CachedDistributionClient.EventsBatcher(mock_distribution_client, "", 0, 0)
    events_batcher.queue.put(None)
    events_batcher._accept_event()
    assert len(events_batcher.events) == 0


def test_stop_events_batcher(mock_distribution_client):
    events_batcher = CachedDistributionClient.EventsBatcher(mock_distribution_client, "", 0, 0)
    events_batcher.stop()
    # Check for termination sentinel value
    assert events_batcher.queue.get_nowait() is None
