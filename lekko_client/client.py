from abc import ABC, abstractmethod
from argparse import Namespace
from typing import Any, Dict, Optional, Tuple, Type, TypeVar
import os

import grpc
from google.protobuf import descriptor_pool as proto_descriptor_pool, symbol_database
from google.protobuf import symbol_database as proto_symbol_database
from google.protobuf.any_pb2 import Any as AnyProto
from google.protobuf.message import Message as ProtoMessage


from lekko_client import LEKKO_API_URL, LEKKO_SIDECAR_URL
from lekko_client.exceptions import (
    AuthenticationError,
    FeatureNotFound,
    MismatchedProtoType,
    MismatchedType,
)
from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2 import (
    GetBoolValueRequest,
    GetStringValueRequest,
    GetIntValueRequest,
    GetFloatValueRequest,
    GetJSONValueRequest,
    GetProtoValueRequest,
    RepositoryKey,
    RegisterRequest,
)
from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2_grpc import (
    ConfigurationServiceStub,
)
from lekko_client.helpers import ApiKeyInterceptor, convert_context


class Client(ABC):
    ProtoType = TypeVar("ProtoType", bound=ProtoMessage)

    def __init__(
        self,
        owner_name: str,
        repo_name: str,
        namespace: str,
        api_key: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        self.owner_name = owner_name
        self.repo_name = repo_name
        self.namespace = namespace
        self.context = context or {}

        self.api_key = api_key or os.environ.get("LEKKO_API_KEY")

    @abstractmethod
    def get_bool(self, key: str, context: Dict[str, Any]) -> bool:
        raise NotImplemented

    @abstractmethod
    def get_int(self, key: str, context: Dict[str, Any]) -> int:
        raise NotImplemented

    @abstractmethod
    def get_float(self, key: str, context: Dict[str, Any]) -> float:
        raise NotImplemented

    @abstractmethod
    def get_string(self, key: str, context: Dict[str, Any]) -> str:
        raise NotImplemented

    @abstractmethod
    def get_json(self, key: str, context: Dict[str, Any]) -> dict:
        pass

    @abstractmethod
    def get_proto(
        self,
        key: str,
        context: Dict[str, Any],
    ) -> ProtoMessage:
        pass

    @abstractmethod
    def get_proto_by_type(
        self,
        key: str,
        context: Dict[str, Any],
        proto_message_type: Type[ProtoType] = AnyProto,
    ) -> ProtoType:
        pass


class GRPCClient(Client):
    _channels: Dict[Tuple[str, str], grpc.Channel] = {}
    ReturnType = TypeVar("ReturnType", str, float, int, bool, dict, AnyProto)
    _TYPE_MAPPING: Dict[Type, Tuple[str, Type]] = {
        bool: ("GetBoolValue", GetBoolValueRequest),
        int: ("GetIntValue", GetIntValueRequest),
        str: ("GetStringValue", GetStringValueRequest),
        float: ("GetFloatValue", GetFloatValueRequest),
        dict: ("GetJSONValue", GetJSONValueRequest),
        AnyProto: ("GetProtoValue", GetProtoValueRequest),
    }

    def __init__(
        self,
        uri: str,
        owner_name: str,
        repo_name: str,
        namespace: str,
        api_key: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        credentials: Optional[grpc.ChannelCredentials] = None,
    ):
        super().__init__(owner_name, repo_name, namespace, api_key)
        self.repository = RepositoryKey(owner_name=owner_name, repo_name=repo_name)
        self.api_key = api_key or os.environ.get("LEKKO_API_KEY")

        self.namespace = namespace
        self.context = context or {}
        self.uri = uri

        if not self.api_key:
            raise AuthenticationError("Must provide API key and URI")

        init = False
        if (self.uri, self.api_key) not in GRPCClient._channels:
            if credentials:
                channel = grpc.secure_channel(uri, credentials)
            else:
                channel = grpc.insecure_channel(uri)

            channel = grpc.intercept_channel(channel, *[ApiKeyInterceptor(api_key)])
            GRPCClient._channels[(self.uri, self.api_key)] = channel
            init = True

        channel = GRPCClient._channels[(self.uri, self.api_key)]
        self._client = ConfigurationServiceStub(channel)
        if init:
            try:
                self._client.Register(
                    RegisterRequest(
                        repo_key=self.repository, namespace_list=[namespace]
                    )
                )
            except grpc.RpcError:
                # TODO:SAM - re-registering shouldn't cause errors in the future
                pass

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

    def get_proto(self, key: str, context: Dict[str, Any]) -> ProtoMessage:
        val = self._get(key, context, AnyProto)
        db = proto_symbol_database.SymbolDatabase(pool=proto_descriptor_pool.Default())
        try:
            ret_val = db.GetSymbol(val.type_url.split("/")[1])()
            if val.Unpack(ret_val):
                return ret_val
        except (KeyError, IndexError):
            pass
        return val

    def get_proto_by_type(
        self,
        key: str,
        context: Dict[str, Any],
        proto_message_type: Type[Client.ProtoType] = AnyProto,
    ) -> Client.ProtoType:
        val = self._get(key, context, AnyProto)
        ret_val = proto_message_type()
        if val.Unpack(ret_val):
            return ret_val

        raise MismatchedProtoType(
            f"Error unpacking from {val.type_url} to {proto_message_type.DESCRIPTOR.name}"
        )

    def _get(
        self, key: str, context: Dict[str, Any], typ: Type[ReturnType]
    ) -> ReturnType:
        ctx = self.context | context
        fn_name, req_type = self._TYPE_MAPPING[typ]
        try:
            req = req_type(
                key=key,
                context=convert_context(ctx),
                namespace=self.namespace,
                repo_key=self.repository,
            )
            response = getattr(self._client, fn_name)(req)
            return response.value
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                if "type mismatch" in e.details():
                    raise MismatchedType(e.details()) from e
                elif "not found" in e.details():
                    raise FeatureNotFound(e.details()) from e
            raise


class SidecarClient(GRPCClient):
    def __init__(
        self,
        owner_name: str,
        repo_name: str,
        namespace: str,
        api_key: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        uri: str = LEKKO_SIDECAR_URL,
    ):
        super().__init__(uri, owner_name, repo_name, namespace, api_key, context)


class APIClient(GRPCClient):
    def __init__(
        self,
        owner_name: str,
        repo_name: str,
        namespace: str,
        api_key: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        uri: str = LEKKO_API_URL,
        credentials: grpc.ChannelCredentials = grpc.ssl_channel_credentials(),
    ):
        super().__init__(
            uri, owner_name, repo_name, namespace, api_key, context, credentials
        )
