import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type, TypeVar

from google.protobuf.message import Message as ProtoMessage


class Client(ABC):
    ProtoType = TypeVar("ProtoType", bound=ProtoMessage)

    def __init__(
        self,
        owner_name: str,
        repo_name: str,
        api_key: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        local: bool = False,
    ):
        self.owner_name = owner_name
        self.repo_name = repo_name
        self.context = context or {}

        if local:
            self.api_key = None
        else:
            self.api_key = api_key or os.environ.get("LEKKO_API_KEY")

    @abstractmethod
    def get_bool(self, namespace: str, key: str, context: Dict[str, Any]) -> bool:
        ...

    @abstractmethod
    def get_int(self, namespace: str, key: str, context: Dict[str, Any]) -> int:
        ...

    @abstractmethod
    def get_float(self, namespace: str, key: str, context: Dict[str, Any]) -> float:
        ...

    @abstractmethod
    def get_string(self, namespace: str, key: str, context: Dict[str, Any]) -> str:
        ...

    @abstractmethod
    def get_json(self, namespace: str, key: str, context: Dict[str, Any]) -> dict:
        ...

    @abstractmethod
    def get_proto(
        self,
        namsespace: str,
        key: str,
        context: Dict[str, Any],
    ) -> ProtoMessage:
        ...

    @abstractmethod
    def get_proto_by_type(
        self,
        namsespace: str,
        key: str,
        context: Dict[str, Any],
        proto_message_type: Type[ProtoType],
    ) -> ProtoType:
        ...

    @abstractmethod
    def close(self):
        ...
