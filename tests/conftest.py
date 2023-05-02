import concurrent.futures.thread
from concurrent.futures import ThreadPoolExecutor
from unittest import mock

import grpc
import grpc_testing
import pytest

from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2 import (
    DESCRIPTOR,
    GetBoolValueResponse,
    GetFloatValueResponse,
    GetIntValueResponse,
    GetJSONValueResponse,
    GetProtoValueResponse,
    GetStringValueResponse,
    RegisterResponse,
)
from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2_grpc import (
    ConfigurationServiceServicer,
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
def test_channel(test_thread):
    channel = grpc_testing.channel(DESCRIPTOR.services_by_name.values(), grpc_testing.strict_real_time())
    try:
        with mock.patch("lekko_client.client.get_grpc_channel", return_value=(channel, False)):
            yield channel
    finally:
        channel.close()


class MockServer:
    def __init__(self, channel, thread):
        self.channel = channel
        self.thread = thread

    def mock_async_response(self, fn_name, response, status_code=grpc.StatusCode.OK, error_text=""):
        def server():
            service = DESCRIPTOR.services_by_name["ConfigurationService"]
            _, request, rpc = self.channel.take_unary_unary(service.methods_by_name[fn_name])
            rpc.terminate(response, [], status_code, error_text)
            return request

        server_future = self.thread.submit(server)
        return server_future


@pytest.fixture
def test_server(test_channel, test_thread):
    return MockServer(test_channel, test_thread)
