"""Lekko Python SDK Client"""

from enum import Enum
from typing import Any, Dict, Optional, Type

from google.protobuf.message import Message as ProtoMessage

from lekko_client import exceptions
from lekko_client.clients import (
    APIClient,
    CachedBackendClient,
    CachedGitClient,
    Client,
    SidecarClient,
)
from lekko_client.constants import LEKKO_API_URL, LEKKO_SIDECAR_URL  # noqa
from lekko_client.stores import MemoryStore

__version__ = "0.1.4"

__client: Client


class Mode(Enum):
    API = 1
    SIDECAR = 2
    CACHED_SERVER = 3
    CACHED_GIT = 4


def initialize(
    mode: Mode,
    owner_name: str,
    repo_name: str,
    api_key: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    git_repo_path: Optional[str] = None,
) -> Client:
    global __client
    if mode == Mode.API:
        __client = APIClient(owner_name, repo_name, api_key, context)
    elif mode == Mode.SIDECAR:
        __client = SidecarClient(owner_name, repo_name, api_key, context)
    elif mode == Mode.CACHED_GIT:
        if not git_repo_path:
            raise exceptions.GitRepoNotFound("Must provide a path to git repo in Cached Git mode")
        __client = CachedGitClient(LEKKO_API_URL, owner_name, repo_name, MemoryStore(), git_repo_path, api_key, context)
    elif mode == Mode.CACHED_SERVER:
        __client = CachedBackendClient(LEKKO_API_URL, owner_name, repo_name, MemoryStore(), api_key, context)
    else:
        raise exceptions.LekkoError("Unknown client mode")
    return __client


def get_bool(namespace: str, key: str, context: Dict[str, Any]) -> bool:
    return __client.get_bool(namespace, key, context)


def get_int(namespace: str, key: str, context: Dict[str, Any]) -> int:
    return __client.get_int(namespace, key, context)


def get_float(namespace: str, key: str, context: Dict[str, Any]) -> float:
    return __client.get_float(namespace, key, context)


def get_string(namespace: str, key: str, context: Dict[str, Any]) -> str:
    return __client.get_string(namespace, key, context)


def get_json(namespace: str, key: str, context: Dict[str, Any]) -> dict:
    return __client.get_json(namespace, key, context)


def get_proto(
    namespace: str,
    key: str,
    context: Dict[str, Any],
) -> ProtoMessage:
    return __client.get_proto(namespace, key, context)


def get_proto_by_type(
    namespace: str,
    key: str,
    context: Dict[str, Any],
    proto_message_type: Type[Client.ProtoType],
) -> Client.ProtoType:
    return __client.get_proto_by_type(namespace, key, context, proto_message_type)
