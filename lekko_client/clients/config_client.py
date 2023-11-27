import json
from typing import Any, Callable, Dict, Optional, Tuple, Type, TypeVar

import grpc
from google.protobuf import descriptor_pool as proto_descriptor_pool
from google.protobuf import symbol_database as proto_symbol_database
from google.protobuf.any_pb2 import Any as AnyProto
from google.protobuf.message import Message as ProtoMessage

from lekko_client.clients.client import Client
from lekko_client.constants import LEKKO_API_URL, LEKKO_SIDECAR_URL
from lekko_client.exceptions import (
    AuthenticationError,
    ConfigNotFound,
    MismatchedProtoType,
    MismatchedType,
)
from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2 import (
    DeregisterRequest,
    GetBoolValueRequest,
    GetFloatValueRequest,
    GetIntValueRequest,
    GetJSONValueRequest,
    GetProtoValueRequest,
    GetStringValueRequest,
    RegisterRequest,
    RepositoryKey,
)
from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2_grpc import (
    ConfigurationServiceStub,
)
from lekko_client.helpers import convert_context, get_grpc_channel

ReturnType = TypeVar("ReturnType")

RequestType = TypeVar(
    "RequestType",
    GetBoolValueRequest,
    GetIntValueRequest,
    GetStringValueRequest,
    GetFloatValueRequest,
    GetJSONValueRequest,
    GetProtoValueRequest,
)


class JsonBytes(bytes):
    pass


class ConfigServiceClient(Client):
    _channels: Dict[Tuple[str, str], grpc.Channel] = {}

    def __init__(
        self,
        uri: str,
        owner_name: str,
        repo_name: str,
        api_key: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        credentials: Optional[grpc.ChannelCredentials] = None,
    ):
        super().__init__(owner_name, repo_name, api_key)
        self.repository = RepositoryKey(owner_name=owner_name, repo_name=repo_name)

        self.context = context or {}
        self.uri = uri

        if not self.api_key:
            raise AuthenticationError("Must provide API key and URI")

        channel = get_grpc_channel(self.uri, self.api_key, credentials)

        self._client = ConfigurationServiceStub(channel)
        try:
            self._client.Register(RegisterRequest(repo_key=self.repository, namespace_list=[]))
        except grpc.RpcError:
            # TODO:SAM - re-registering shouldn't cause errors in the future
            pass

    def close(self) -> None:
        super().close()
        self._client.Deregister(DeregisterRequest())

    def get_bool(self, namespace: str, key: str, context: dict[str, Any]) -> bool:
        return self._get(namespace, key, context, GetBoolValueRequest, self._client.GetBoolValue).value

    def get_int(self, namespace: str, key: str, context: dict[str, Any]) -> int:
        return self._get(namespace, key, context, GetIntValueRequest, self._client.GetIntValue).value

    def get_float(self, namespace: str, key: str, context: dict[str, Any]) -> float:
        return self._get(namespace, key, context, GetFloatValueRequest, self._client.GetFloatValue).value

    def get_string(self, namespace: str, key: str, context: dict[str, Any]) -> str:
        return self._get(namespace, key, context, GetStringValueRequest, self._client.GetStringValue).value

    def get_json(self, namespace: str, key: str, context: dict[str, Any]) -> Any:
        json_bytes = self._get(namespace, key, context, GetJSONValueRequest, self._client.GetJSONValue).value
        return json.loads(json_bytes.decode("utf-8"))

    def get_proto(self, namespace: str, key: str, context: dict[str, Any]) -> ProtoMessage:
        val = self._get_proto(namespace, key, context)
        db = proto_symbol_database.SymbolDatabase(pool=proto_descriptor_pool.Default())  # type: ignore
        try:
            ret_val = db.GetSymbol(val.type_url.split("/")[1])()
            if val.Unpack(ret_val):
                return ret_val
        except (KeyError, IndexError):
            pass
        return val

    def get_proto_by_type(
        self,
        namespace: str,
        key: str,
        context: Dict[str, Any],
        proto_message_type: Type[Client.ProtoType],
    ) -> Client.ProtoType:
        val = self._get_proto(namespace, key, context)
        ret_val = proto_message_type()
        if val.Unpack(ret_val):
            return ret_val

        raise MismatchedProtoType(f"Error unpacking from {val.type_url} to {proto_message_type.DESCRIPTOR.name}")

    def _get(
        self,
        namespace: str,
        key: str,
        context: Dict[str, Any],
        req_type: Type[RequestType],
        fn: Callable[[RequestType], ReturnType],
    ) -> ReturnType:
        ctx = self.context | context
        try:
            req = req_type(
                key=key,
                context=convert_context(ctx),
                namespace=namespace,
                repo_key=self.repository,
            )
            response = fn(req)
            return response
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise ConfigNotFound(e.details()) from e
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise MismatchedType(e.details()) from e
            raise

    def _get_proto(self, namespace: str, key: str, context: dict[str, Any]) -> AnyProto:
        ctx = self.context | context
        try:
            req = GetProtoValueRequest(
                key=key,
                context=convert_context(ctx),
                namespace=namespace,
                repo_key=self.repository,
            )
            response = self._client.GetProtoValue(req)
            if response.value_v2.IsInitialized() and response.value_v2.type_url:
                return AnyProto(
                    type_url=response.value_v2.type_url,
                    value=response.value_v2.value,
                )
            return response.value
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise ConfigNotFound(e.details()) from e
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                raise MismatchedType(e.details()) from e
            raise


class SidecarClient(ConfigServiceClient):
    def __init__(
        self,
        owner_name: str,
        repo_name: str,
        api_key: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        uri: str = LEKKO_SIDECAR_URL,
    ):
        super().__init__(uri, owner_name, repo_name, api_key, context)


class APIClient(ConfigServiceClient):
    def __init__(
        self,
        owner_name: str,
        repo_name: str,
        api_key: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        uri: str = LEKKO_API_URL,
        credentials: grpc.ChannelCredentials = grpc.ssl_channel_credentials(),
    ):
        super().__init__(
            uri,
            owner_name,
            repo_name,
            api_key,
            context,
            credentials,
        )
