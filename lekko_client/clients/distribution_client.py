import json
from abc import abstractmethod
from typing import Any, Dict, Optional, Type, TypeVar, Union

import grpc
from google.protobuf import descriptor_pool as proto_descriptor_pool
from google.protobuf import symbol_database as proto_symbol_database
from google.protobuf.any_pb2 import Any as ProtoAny
from google.protobuf.json_format import MessageToJson
from google.protobuf.message import Message as ProtoMessage
from google.protobuf.struct_pb2 import Value
from google.protobuf.wrappers_pb2 import BoolValue, FloatValue, Int64Value, StringValue

from lekko_client.clients.client import Client
from lekko_client.evaluation.evaluation import evaluate
from lekko_client.exceptions import MismatchedProtoType
from lekko_client.gen.lekko.backend.v1beta1.distribution_service_pb2 import (
    DeregisterClientRequest,
    GetRepositoryContentsResponse,
    RegisterClientRequest,
    RepositoryKey,
)
from lekko_client.gen.lekko.backend.v1beta1.distribution_service_pb2_grpc import (
    DistributionServiceStub,
)
from lekko_client.helpers import convert_context, get_grpc_channel
from lekko_client.stores.store import Store


class CachedDistributionClient(Client):
    def __init__(
        self,
        uri: str,
        owner_name: str,
        repo_name: str,
        store: Store,
        api_key: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        credentials: grpc.ChannelCredentials = grpc.ssl_channel_credentials(),
    ):
        from lekko_client import __version__

        super().__init__(owner_name, repo_name, api_key, context)
        self.uri = uri
        self.repository = RepositoryKey(owner_name=owner_name, repo_name=repo_name)
        self.store = store
        self._client = None
        if self.api_key:
            channel = get_grpc_channel(self.uri, self.api_key, credentials)
            self._client = DistributionServiceStub(channel)
            register_response = self._client.RegisterClient(
                RegisterClientRequest(repo_key=self.repository, sidecar_version=__version__)
            )
            self.session_key = register_response.session_key
            # if self.events_batcher:
            # await self.events_batcher.init(self.session_key)
        self.initialize()

    _TYPE_MAPPING: Dict[Type, Type[Union[BoolValue, Int64Value, StringValue, FloatValue]]] = {
        bool: BoolValue,
        int: Int64Value,
        str: StringValue,
        float: FloatValue,
    }

    @abstractmethod
    def initialize(self):
        ...

    def load(self) -> bool:
        contents = self.get_contents()
        if not contents:
            return False
        loaded = self.store.load(contents)
        return loaded

    @abstractmethod
    def get_contents(self) -> Optional[GetRepositoryContentsResponse]:
        ...

    def _get(self, namespace: str, key: str, context: Dict[str, Any]) -> ProtoAny:
        feature_data = self.store.get(namespace, key)
        result = evaluate(feature_data.feature, namespace, convert_context(context))
        return result.value

    ReturnType = TypeVar("ReturnType", str, float, int, bool)

    def _get_scalar(self, namespace: str, key: str, context: Dict[str, Any], typ: Type[ReturnType]) -> ReturnType:
        result = self._get(namespace, key, context)
        return_wrapper = self._TYPE_MAPPING[typ]()
        result.Unpack(return_wrapper)
        return return_wrapper.value  # type:ignore

    def get_bool(self, namespace: str, key: str, context: Dict[str, Any]) -> bool:
        return self._get_scalar(namespace, key, context, bool)

    def get_int(self, namespace: str, key: str, context: Dict[str, Any]) -> int:
        return self._get_scalar(namespace, key, context, int)

    def get_float(self, namespace: str, key: str, context: Dict[str, Any]) -> float:
        return self._get_scalar(namespace, key, context, float)

    def get_string(self, namespace: str, key: str, context: Dict[str, Any]) -> str:
        return self._get_scalar(namespace, key, context, str)

    def get_json(self, namespace: str, key: str, context: Dict[str, Any]) -> Any:
        result = self._get(namespace, key, context)
        return_wrapper = Value()
        result.Unpack(return_wrapper)
        return json.loads(MessageToJson(return_wrapper))

    def get_proto(self, namespace: str, key: str, context: Dict[str, Any]) -> ProtoMessage:
        val = self._get(namespace, key, context)
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
        namespace: str,
        key: str,
        context: Dict[str, Any],
        proto_message_type: Type[Client.ProtoType],
    ) -> Client.ProtoType:
        val = self._get(namespace, key, context)
        ret_val = proto_message_type()
        if val.Unpack(ret_val):
            return ret_val

        raise MismatchedProtoType(f"Error unpacking from {val.type_url} to {proto_message_type.DESCRIPTOR.name}")

    # def track(self, namespace: str, key: str, result: StoredEvalResult, ctx: Optional[ClientContext] = None):
    #    if not self.events_batcher:
    #        return
    #    self.events_batcher.track(FlagEvaluationEvent(
    #        repo_key=self.repo_key,
    #        commit_sha=result.commit_sha,
    #        feature_sha=result.config_sha,
    #        namespace_name=namespace,
    #        feature_name=key,
    #        context_keys=to_context_keys_proto(ctx),
    #        result_path=result.eval_result.path,
    #        client_event_time=Timestamp.now()
    #    ))

    def close(self):
        if self._client and self.session_key:
            self._client.DeregisterClient(DeregisterClientRequest(session_key=self.session_key))
