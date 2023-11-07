from typing import Any, Dict, List, Optional, Tuple

import grpc
from grpc_interceptor import ClientCallDetails, ClientInterceptor
from grpc_interceptor.client import ClientInterceptorReturnType

from lekko_client.gen.lekko.backend.v1beta1.distribution_service_pb2 import ContextKey
from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2 import Value
from lekko_client.models import ClientContext


def convert_context(context: dict[str, Any]) -> ClientContext:
    def convert_value(val: Any) -> Value:
        if isinstance(val, bool):
            return Value(bool_value=val)
        elif isinstance(val, int):
            return Value(int_value=val)
        elif isinstance(val, float):
            return Value(double_value=val)
        else:
            return Value(string_value=str(val))

    return {k: convert_value(v) for k, v in context.items()}


def get_value_type(val: Value) -> str:
    return (val.WhichOneof("kind") or "").removesuffix("_value")


def get_context_keys(context: Optional[ClientContext] = None) -> List[ContextKey]:
    if not context:
        return []

    return [ContextKey(key=k, type=get_value_type(v)) for k, v in context.items()]


class ApiKeyInterceptor(ClientInterceptor):
    """A test interceptor that injects invocation metadata."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def intercept(self, method, request_or_iterator, call_details) -> ClientInterceptorReturnType:
        new_details = ClientCallDetails(
            call_details.method,
            call_details.timeout,
            [("apikey", self.api_key)],
            call_details.credentials,
            call_details.wait_for_ready,
            call_details.compression,
        )

        return method(request_or_iterator, new_details)


_CHANNELS: Dict[Tuple[str, Optional[str]], grpc.Channel] = {}


def get_grpc_channel(
    url: str, api_key: Optional[str] = None, credentials: Optional[grpc.ChannelCredentials] = None
) -> grpc.Channel:
    if (url, api_key) not in _CHANNELS:
        if credentials:
            channel = grpc.secure_channel(url, credentials)
        else:
            channel = grpc.insecure_channel(url)

        if api_key:
            channel = grpc.intercept_channel(channel, *[ApiKeyInterceptor(api_key)])
        _CHANNELS[(url, api_key)] = channel

    return _CHANNELS[(url, api_key)]
