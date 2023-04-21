from typing import Any, Dict

import grpc

from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2 import GetBoolValueRequest, GetStringValueRequest, GetIntValueRequest, GetJSONValueRequest, RepositoryKey
from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2_grpc import ConfigurationServiceStub
from lekko_client.helpers import ApiKeyInterceptor, convert_context


class Client:
    _channels: Dict[str, grpc.Channel] = {}

    def __init__(self, uri: str, api_key: str, owner_name: str, repo_name: str, namespace: str, context: Dict[str, Any]):

        self.repository = RepositoryKey(owner_name=owner_name, repo_name=repo_name)
        self.api_key = api_key
        self.namespace = namespace
        self.context = context
        if uri not in Client._channels:
            channel = grpc.insecure_channel(uri)
            channel = grpc.intercept_channel(channel, *[ApiKeyInterceptor(api_key)])
            Client._channels[uri] = channel
        channel = Client._channels[uri]
        self._client = ConfigurationServiceStub(channel)

    def get_bool(self, key: str, context: Dict[str, Any]) -> bool:
        ctx = self.context | context
        return self._client.GetBoolValue(GetBoolValueRequest(key=key, context=convert_context(ctx), namespace=self.namespace, repo_key=self.repository)).value

    def get_int(self, key: str, context: Dict[str, Any]) -> int:
        ctx = self.context | context
        return self._client.GetIntValue(GetIntValueRequest(key=key, context=convert_context(ctx), namespace=self.namespace, repo_key=self.repository)).value

    def get_string(self, key: str, context: Dict[str, Any]) -> str:
        ctx = self.context | context
        return self._client.GetStringValue(GetStringValueRequest(key=key, context=convert_context(ctx), namespace=self.namespace, repo_key=self.repository)).value

    def get_json(self, key: str, context: Dict[str, Any]) -> dict:
        ctx = self.context | context
        return self._client.GetJSONValue(GetJSONValueRequest(key=key, context=convert_context(ctx), namespace=self.namespace, repo_key=self.repository)).value
