import concurrent.futures.thread
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any, List, Tuple
from unittest import mock

import grpc
import grpc_testing
import pytest
from google.protobuf.any_pb2 import Any as ProtoAny
from google.protobuf.message import Message as ProtoMessage
from google.protobuf.struct_pb2 import Struct, Value
from google.protobuf.wrappers_pb2 import Int64Value
from grpc_testing import _channel  # noqa

from lekko_client import helpers
from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2 import DESCRIPTOR
from lekko_client.gen.lekko.feature.v1beta1.feature_pb2 import Any as LekkoAny
from lekko_client.gen.lekko.feature.v1beta1.feature_pb2 import (
    Constraint,
    Feature,
    FeatureType,
    Tree,
)
from lekko_client.gen.lekko.rules.v1beta3.rules_pb2 import (
    Atom,
    ComparisonOperator,
    Rule,
)


@pytest.fixture
def test_thread():
    client_execution_thread_pool = ThreadPoolExecutor(max_workers=2)

    try:
        yield client_execution_thread_pool
    finally:
        client_execution_thread_pool.shutdown(wait=False)
        client_execution_thread_pool._threads.clear()
        concurrent.futures.thread._threads_queues.clear()


@pytest.fixture
def test_channel_no_interceptor(test_thread):
    channel = grpc_testing.channel(DESCRIPTOR.services_by_name.values(), grpc_testing.strict_real_time())
    try:
        with mock.patch("lekko_client.client.get_grpc_channel", return_value=channel):
            yield channel
    finally:
        channel.close()


@pytest.fixture
def test_channel(test_thread):
    channel = grpc_testing.channel(DESCRIPTOR.services_by_name.values(), grpc_testing.strict_real_time())
    try:
        with mock.patch("grpc.insecure_channel", return_value=channel), mock.patch(
            "grpc.secure_channel", return_value=channel
        ):
            yield channel
    finally:
        channel.close()


class PatchedUnaryUnary(grpc_testing._channel._multi_callable.UnaryUnary):
    # grpc_testing is very out of date and its fn sigs don't take wait_for_ready or compression
    def with_call(self, request, timeout=None, metadata=None, credentials=None, wait_for_ready=None, compression=None):
        return super().with_call(request, timeout, metadata, credentials)


grpc_testing._channel._channel._multi_callable.UnaryUnary = PatchedUnaryUnary


class MockServer:
    def __init__(self, channel, thread):
        self.channel = channel
        self.thread = thread
        helpers._CHANNELS = {}

    @dataclass
    class MockRequestResponse:
        fn_name: str
        response: ProtoMessage
        status_code: grpc.StatusCode = grpc.StatusCode.OK
        error_text: str = ""

    @dataclass
    class CompletedRequest:
        arg: ProtoMessage
        metadata: Tuple[Tuple[str, str]]

    def mock_async_responses(self, mock_requests: List[MockRequestResponse]):
        def server() -> List[MockServer.CompletedRequest]:
            service = DESCRIPTOR.services_by_name["ConfigurationService"]
            incoming_requests = []
            for mock_request in mock_requests:
                metadata, request, rpc = self.channel.take_unary_unary(service.methods_by_name[mock_request.fn_name])
                rpc.terminate(mock_request.response, [], mock_request.status_code, mock_request.error_text)
                incoming_requests.append(MockServer.CompletedRequest(arg=request, metadata=metadata))

            return incoming_requests

        server_future = self.thread.submit(server)
        return server_future


@pytest.fixture
def test_server(test_channel, test_thread):
    return MockServer(test_channel, test_thread)


@pytest.fixture
def test_server_no_interceptor(test_channel_no_interceptor, test_thread):
    return MockServer(test_channel_no_interceptor, test_thread)


@pytest.fixture
def test_complex_rule_feature():
    filename = "tests/fixtures/rules.proto.bin"
    feature = Feature()
    with open(filename, "rb") as f:
        feature.ParseFromString(f.read())

    return feature


@pytest.fixture
def test_feature_default_value() -> ProtoAny:
    any_proto = ProtoAny()
    any_proto.Pack(Int64Value(value=1))
    return any_proto


@pytest.fixture
def test_feature_constraint_value() -> ProtoAny:
    any_proto = ProtoAny()
    any_proto.Pack(Int64Value(value=2))
    return any_proto


def convert_to_value(v: Any) -> Value:
    s = Struct()
    s.update({"key": v})
    return s.fields["key"]


@pytest.fixture
def test_feature_no_constraints(test_feature_default_value) -> Feature:
    return Feature(
        key="key",
        description="config description",
        type=FeatureType.FEATURE_TYPE_INT,
        tree=Tree(
            default=test_feature_default_value,
            default_new=LekkoAny(type_url=test_feature_default_value.type_url, value=test_feature_default_value.value),
        ),
    )


@pytest.fixture
def test_feature_one_level_traversal(test_feature_default_value, test_feature_constraint_value) -> Feature:
    return Feature(
        key="key",
        description="config description",
        type=FeatureType.FEATURE_TYPE_INT,
        tree=Tree(
            default=test_feature_default_value,
            default_new=LekkoAny(type_url=test_feature_default_value.type_url, value=test_feature_default_value.value),
            constraints=[
                Constraint(
                    rule_ast_new=Rule(
                        atom=Atom(
                            context_key="age",
                            comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                            comparison_value=convert_to_value(10),
                        )
                    ),
                    value=test_feature_constraint_value,
                    value_new=LekkoAny(
                        type_url=test_feature_constraint_value.type_url, value=test_feature_constraint_value.value
                    ),
                ),
                Constraint(
                    rule_ast_new=Rule(
                        atom=Atom(
                            context_key="age",
                            comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                            comparison_value=convert_to_value(12),
                        )
                    ),
                    value=test_feature_constraint_value,
                    value_new=LekkoAny(
                        type_url=test_feature_constraint_value.type_url, value=test_feature_constraint_value.value
                    ),
                ),
            ],
        ),
    )


@pytest.fixture
def test_feature_two_level_traversal(test_feature_default_value, test_feature_constraint_value) -> Feature:
    return Feature(
        key="key",
        description="config description",
        type=FeatureType.FEATURE_TYPE_INT,
        tree=Tree(
            default=test_feature_default_value,
            default_new=LekkoAny(type_url=test_feature_default_value.type_url, value=test_feature_default_value.value),
            constraints=[
                Constraint(
                    rule_ast_new=Rule(
                        atom=Atom(
                            context_key="age",
                            comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                            comparison_value=convert_to_value(10),
                        )
                    ),
                    value=test_feature_constraint_value,
                    value_new=LekkoAny(
                        type_url=test_feature_constraint_value.type_url, value=test_feature_constraint_value.value
                    ),
                    constraints=[
                        Constraint(
                            rule_ast_new=Rule(
                                atom=Atom(
                                    context_key="city",
                                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                                    comparison_value=convert_to_value("Rome"),
                                )
                            ),
                            value=test_feature_constraint_value,
                            value_new=LekkoAny(
                                type_url=test_feature_constraint_value.type_url,
                                value=test_feature_constraint_value.value,
                            ),
                        ),
                        Constraint(
                            rule_ast_new=Rule(
                                atom=Atom(
                                    context_key="city",
                                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                                    comparison_value=convert_to_value("Paris"),
                                )
                            ),
                            value=test_feature_constraint_value,
                            value_new=LekkoAny(
                                type_url=test_feature_constraint_value.type_url,
                                value=test_feature_constraint_value.value,
                            ),
                        ),
                    ],
                ),
                Constraint(
                    rule_ast_new=Rule(
                        atom=Atom(
                            context_key="age",
                            comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                            comparison_value=convert_to_value(12),
                        )
                    ),
                    value=test_feature_constraint_value,
                    value_new=LekkoAny(
                        type_url=test_feature_constraint_value.type_url, value=test_feature_constraint_value.value
                    ),
                    constraints=[
                        Constraint(
                            rule_ast_new=Rule(
                                atom=Atom(
                                    context_key="city",
                                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                                    comparison_value=convert_to_value("Rome"),
                                )
                            ),
                            value=test_feature_constraint_value,
                            value_new=LekkoAny(
                                type_url=test_feature_constraint_value.type_url,
                                value=test_feature_constraint_value.value,
                            ),
                        ),
                        Constraint(
                            rule_ast_new=Rule(
                                atom=Atom(
                                    context_key="city",
                                    comparison_operator=ComparisonOperator.COMPARISON_OPERATOR_EQUALS,
                                    comparison_value=convert_to_value("Paris"),
                                )
                            ),
                            value=test_feature_constraint_value,
                            value_new=LekkoAny(
                                type_url=test_feature_constraint_value.type_url,
                                value=test_feature_constraint_value.value,
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )
