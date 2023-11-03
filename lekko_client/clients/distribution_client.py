import json
import logging
import time
from abc import abstractmethod
from datetime import datetime
from threading import Thread
from typing import Any, Dict, List, Optional, Type, TypeVar

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
from lekko_client.exceptions import LekkoRpcError, MismatchedProtoType, MismatchedType
from lekko_client.gen.lekko.backend.v1beta1.distribution_service_pb2 import (
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
from lekko_client.helpers import convert_context, get_context_keys, get_grpc_channel
from lekko_client.models import ClientContext, FeatureData
from lekko_client.stores.store import Store


log = logging.getLogger(__name__)


class CachedDistributionClient(Client):
    class EventsBatcher(Thread):
        def __init__(self, dist_client: DistributionServiceStub, session_key: str, upload_interval_ms: int):
            super().__init__()
            self.daemon = True
            self.dist_client = dist_client
            self.upload_interval = upload_interval_ms
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
                    SendFlagEvaluationMetricsRequest(events=self.events, session_key=self.session_key),
                    timeout=10,
                )
            self.events = []

        def run(self):
            # TODO: Lock
            while self._enabled:
                try:
                    self.upload_events()
                except:
                    log.warning("failed to send config evaluation events to lekko")
                time.sleep(self.upload_interval)

    def __init__(
        self,
        uri: str,
        owner_name: str,
        repo_name: str,
        store: Store,
        api_key: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        credentials: grpc.ChannelCredentials = grpc.ssl_channel_credentials(),
        local: bool = False,
    ):
        super().__init__(owner_name, repo_name, api_key, context, local=local)
        self.uri = uri
        self.repository = RepositoryKey(owner_name=owner_name, repo_name=repo_name)
        self.store = store
        self._client: Optional[DistributionServiceStub] = None
        self.session_key = ''
        self.events_batcher = None
        if self.api_key:
            self.initialize_client(credentials)
            if self._client:
                self.events_batcher = self.EventsBatcher(self._client, self.session_key, 15 * 1000)
                self.events_batcher.start()


    _TYPE_MAPPING: Dict[Type, Type[BoolValue | Int64Value | StringValue | FloatValue]] = {
        bool: BoolValue,
        int: Int64Value,
        str: StringValue,
        float: FloatValue,
    }

    def initialize_client(self, credentials: grpc.ChannelCredentials):
        from lekko_client import __version__

        channel = get_grpc_channel(self.uri, self.api_key, credentials)
        self._client = DistributionServiceStub(channel)
        try:
            register_response = self._client.RegisterClient(
                RegisterClientRequest(repo_key=self.repository, sidecar_version=__version__),
                timeout=1,
            )
            self.session_key = register_response.session_key
        except grpc.RpcError as e:
            log.warning("failed to register lekko client")
            # raise LekkoRpcError(f"Unable to register distribution service: {e}")

    @abstractmethod
    def initialize(self) -> None:
        ...

    def load(self) -> bool:
        contents = self.load_contents()
        if not contents:
            return False
        loaded = self.store.load(contents)
        return loaded

    @abstractmethod
    def load_contents(self) -> Optional[GetRepositoryContentsResponse]:
        ...

    def track(
        self, namespace: str, feature_data: FeatureData, result: EvaluationResult, context: Optional[ClientContext]
    ) -> None:
        if not self.events_batcher:
            return

        timestamp = Timestamp()
        timestamp.FromDatetime(datetime.utcnow())
        event = FlagEvaluationEvent(
            repo_key=self.repository,
            commit_sha=self.store.commit_sha,
            feature_sha=feature_data.config_sha,
            namespace_name=namespace,
            feature_name=feature_data.feature.key,
            context_keys=get_context_keys(context),
            result_path=result.path,
            client_event_time=timestamp,
        )
        self.events_batcher.add_event(event)

    def get(self, namespace: str, key: str, context: Dict[str, Any]) -> ProtoAny:
        feature_data = self.store.get(namespace, key)
        client_context = convert_context(context)
        result = evaluate(feature_data.feature, namespace, client_context)
        self.track(namespace, feature_data, result, client_context)
        return result.value

    ReturnType = TypeVar("ReturnType", str, float, int, bool)

    def get_scalar(self, namespace: str, key: str, context: Dict[str, Any], typ: Type[ReturnType]) -> ReturnType:
        result = self.get(namespace, key, context)
        return_wrapper = self._TYPE_MAPPING[typ]()
        if result.Unpack(return_wrapper):
            return return_wrapper.value  # type:ignore
        raise MismatchedType(f"Feature {key} is of type {result.type_url} and cannot be converted to {typ}")

    def get_bool(self, namespace: str, key: str, context: Dict[str, Any]) -> bool:
        return self.get_scalar(namespace, key, context, bool)

    def get_int(self, namespace: str, key: str, context: Dict[str, Any]) -> int:
        return self.get_scalar(namespace, key, context, int)

    def get_float(self, namespace: str, key: str, context: Dict[str, Any]) -> float:
        return self.get_scalar(namespace, key, context, float)

    def get_string(self, namespace: str, key: str, context: Dict[str, Any]) -> str:
        return self.get_scalar(namespace, key, context, str)

    def get_json(self, namespace: str, key: str, context: Dict[str, Any]) -> Any:
        result = self.get(namespace, key, context)
        return_wrapper = Value()
        result.Unpack(return_wrapper)
        return json.loads(MessageToJson(return_wrapper))

    def get_proto(self, namespace: str, key: str, context: Dict[str, Any]) -> ProtoMessage:
        val = self.get(namespace, key, context)
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
        val = self.get(namespace, key, context)
        ret_val = proto_message_type()
        if val.Unpack(ret_val):
            return ret_val

        raise MismatchedProtoType(f"Error unpacking from {val.type_url} to {proto_message_type.DESCRIPTOR.name}")

    def close(self):
        super().close()
        if self._client and self.session_key:
            if self.events_batcher:
                self.events_batcher.upload_events()
                self.events_batcher.stop()
            self._client.DeregisterClient(DeregisterClientRequest(session_key=self.session_key))
