from typing import Any, Dict

from grpc_interceptor import ClientCallDetails, ClientInterceptor

from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2 import Value


def convert_context(context: dict) -> Dict[str, Value]:
    def convert_value(val: Any) -> Value:
        if isinstance(val, bool):
            return Value(bool_value=val)
        elif isinstance(val, int):
            return Value(int_value=val)
        elif isinstance(val, float):
            return Value(double_value=val)
        else:
            return Value(string_value=str(val))

    return {k: convert_value(v) for k, v in context}


class ApiKeyInterceptor(ClientInterceptor):
    """A test interceptor that injects invocation metadata."""

    def __init__(self, api_key):
        self.api_key = api_key

    def intercept(self, method, request_or_iterator, call_details):
        new_details = ClientCallDetails(
            call_details.method,
            call_details.timeout,
            [("apikey", self.api_key)],
            call_details.credentials,
            call_details.wait_for_ready,
            call_details.compression,
        )

        return method(request_or_iterator, new_details)
