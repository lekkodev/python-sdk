import json
import time
from abc import abstractmethod
from datetime import datetime
from threading import Thread
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import grpc
from google.protobuf import descriptor_pool as proto_descriptor_pool
from google.protobuf import symbol_database as proto_symbol_database
from google.protobuf.any_pb2 import Any as ProtoAny
from google.protobuf.json_format import MessageToJson
from google.protobuf.message import Message as ProtoMessage
from google.protobuf.struct_pb2 import Value
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.wrappers_pb2 import BoolValue, FloatValue, Int64Value, StringValue

from lekko_client.clients.client import Client
from lekko_client.evaluation.evaluation import EvaluationResult, evaluate
from lekko_client.evaluation.rules import ClientContext
from lekko_client.exceptions import MismatchedProtoType
from lekko_client.gen.lekko.backend.v1beta1.distribution_service_pb2 import (
    ContextKey,
    DeregisterClientRequest,
    FlagEvaluationEvent,
    GetRepositoryContentsResponse,
    RegisterClientRequest,
    RepositoryKey,
    SendFlagEvaluationMetricsRequest,
)
from lekko_client.gen.lekko.backend.v1beta1.distribution_service_pb2_grpc import (
    DistributionServiceStub,
)
from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2 import (
    Value as LekkoValue,
)
from lekko_client.helpers import convert_context, get_grpc_channel
from lekko_client.models import FeatureData
from lekko_client.stores.store import Store


class CachedDistributionClient(Client):
    class EventsBatcher(Thread):
        def __init__(self, dist_client: DistributionServiceStub, session_key: str, upload_interval: int):
            super().__init__()
            self.daemon = True
            self.dist_client = dist_client
            self.upload_interval = upload_interval
            self.session_key = session_key
            self.events: List[FlagEvaluationEvent] = []
            self._enabled = True

        def stop(self):
            self._enabled = False

        def add_event(self, event: FlagEvaluationEvent):
            self.events.append(event)

        def upload_events(self):
            if self.events:
                self.dist_client.SendFlagEvaluationMetrics(
                    SendFlagEvaluationMetricsRequest(events=self.events, session_key=self.session_key)
                )
            self.events = []

        def run(self):
            # TODO: Lock
            while self._enabled:
                self.upload_events()
                time.sleep(self.upload_interval / 1000)

        @classmethod
        def get_value_type(cls, val: LekkoValue) -> str:
            return (val.WhichOneof("kind") or "").removesuffix("_value")

        @classmethod
        def get_context_keys(cls, context: Optional[ClientContext] = None) -> List[ContextKey]:
            if not context:
                return []

            return [ContextKey(key=k, type=cls.get_value_type(v)) for k, v in context.items()]

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
            self.events_batcher = self.EventsBatcher(self._client, self.session_key, 15)
            self.events_batcher.start()

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

    def track(
        self, namespace: str, feature_data: FeatureData, result: EvaluationResult, context: Optional[ClientContext]
    ) -> None:
        timestamp = Timestamp()
        timestamp.FromDatetime(datetime.utcnow())
        event = FlagEvaluationEvent(
            repo_key=self.repository,
            commit_sha=self.store.commit_sha,
            feature_sha=feature_data.config_sha,
            namespace_name=namespace,
            feature_name=feature_data.feature.key,
            context_keys=self.events_batcher.get_context_keys(context),
            result_path=result.path,
            client_event_time=timestamp,
        )
        self.events_batcher.add_event(event)

    def _get(self, namespace: str, key: str, context: Dict[str, Any]) -> ProtoAny:
        feature_data = self.store.get(namespace, key)
        result = evaluate(feature_data.feature, namespace, convert_context(context))
        self.track(namespace, feature_data, result, context)
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

    def close(self):
        if self._client and self.session_key:
            self.events_batcher.upload_events()
            self.events_batcher.stop()
            self._client.DeregisterClient(DeregisterClientRequest(session_key=self.session_key))
