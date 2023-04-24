from argparse import Namespace
from typing import Any, Dict, Optional, Tuple, Type, TypeVar
import os

import grpc
from lekko_client.exceptions import AuthenticationError, FeatureNotFound, MismatchedType

from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2 import GetBoolValueRequest, GetStringValueRequest, GetIntValueRequest, GetFloatValueRequest, GetJSONValueRequest, RepositoryKey
from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2_grpc import ConfigurationServiceStub
from lekko_client.helpers import ApiKeyInterceptor, convert_context


class Client:
    _channels: Dict[Tuple[str, str], grpc.Channel] = {}
    T = TypeVar("T", str, float, int, bool, dict)
    _TYPE_MAPPING: Dict[Type, Tuple[str, Type]] = {
        bool: ("GetBoolValue", GetBoolValueRequest),
        int: ("GetIntValue", GetIntValueRequest),
        str: ("GetStringValue", GetStringValueRequest),
        float: ("GetFloatValue", GetFloatValueRequest),
        dict: ("GetJSONValue", GetJSONValueRequest),
    }


    def __init__(self, uri: str, owner_name: str, repo_name: str, namespace: str = "default", api_key: Optional[str] = None, context: Optional[Dict[str, Any]] = None, environment: Optional[Dict[str, str]] = None):
        self.environment = environment or os.environ
        self.repository = RepositoryKey(owner_name=owner_name, repo_name=repo_name)
        self.api_key = api_key or self.environment.get("LEKKO_API_KEY")

        self.namespace = namespace
        self.context = context or {}
        self.uri = uri

        if not self.api_key:
            raise AuthenticationError("Must provide API key and URI")

        if (self.uri, self.api_key) not in Client._channels:
            channel = grpc.insecure_channel(uri)
            channel = grpc.intercept_channel(channel, *[ApiKeyInterceptor(api_key)])
            Client._channels[(self.uri, self.api_key)] = channel
        channel = Client._channels[(self.uri, self.api_key)]
        self._client = ConfigurationServiceStub(channel)

    def get_bool(self, key: str, context: Dict[str, Any]) -> bool:
        return self._get(key, context, bool)

    def get_int(self, key: str, context: Dict[str, Any]) -> int:
        return self._get(key, context, int)

    def get_float(self, key: str, context: Dict[str, Any]) -> float:
        return self._get(key, context, float)

    def get_string(self, key: str, context: Dict[str, Any]) -> str:
        return self._get(key, context, str)

    def get_json(self, key: str, context: Dict[str, Any]) -> dict:
        return self._get(key, context, dict)

    def _get(self, key: str, context: Dict[str, Any], typ: Type[T]) -> T:
        ctx = self.context | context
        fn_name, req_type = self._TYPE_MAPPING[typ]
        try:
            req = req_type(key=key, context=convert_context(ctx), namespace=self.namespace, repo_key=self.repository)
            response = getattr(self._client, fn_name)(req)
            return response.value
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                if "type mismatch" in e.details():
                    raise MismatchedType(e.details()) from e
                elif "not found" in e.details():
                    raise FeatureNotFound(e.details()) from e
            raise
