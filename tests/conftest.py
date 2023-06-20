import concurrent.futures.thread
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import List, Tuple
from unittest import mock

import grpc
import grpc_testing
import pytest
from google.protobuf.message import Message as ProtoMessage
from grpc_testing import _channel  # noqa

from lekko_client import helpers
from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2 import DESCRIPTOR


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
