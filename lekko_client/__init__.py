"""Lekko Python SDK Client"""

import functools
import logging
from dataclasses import dataclass
from threading import RLock
from typing import Any, Callable, Dict, Optional, Type, TypeVar, cast

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
from lekko_client.stores.memory import MemoryStore

__version__ = "0.2.0"

logging.getLogger(__name__).addHandler(logging.NullHandler())

__client: Optional[Client] = None
__client_lock = RLock()


@dataclass(kw_only=True)
class Config:
    owner_name: str
    repo_name: str
    api_key: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    lekko_uri: str = LEKKO_API_URL


@dataclass(kw_only=True)
class SidecarConfig(Config):
    lekko_uri = LEKKO_SIDECAR_URL


@dataclass(kw_only=True)
class APIConfig(Config):
    pass


@dataclass(kw_only=True)
class CachedServerConfig(Config):
    pass


@dataclass(kw_only=True)
class CachedGitConfig(Config):
    git_repo_path: str


def initialize(config: Config) -> Client:
    global __client
    with __client_lock:
        if __client:
            __client.close()
        match config:
            case APIConfig():
                __client = APIClient(
                    owner_name=config.owner_name,
                    repo_name=config.repo_name,
                    api_key=config.api_key,
                    context=config.context,
                )
            case SidecarConfig():
                __client = SidecarClient(
                    owner_name=config.owner_name,
                    repo_name=config.repo_name,
                    api_key=config.api_key,
                    context=config.context,
                )
            case CachedGitConfig():
                __client = CachedGitClient(
                    config.lekko_uri,
                    config.owner_name,
                    config.repo_name,
                    MemoryStore(),
                    config.git_repo_path,
                    config.api_key,
                    config.context,
                )
            case CachedServerConfig():
                __client = CachedBackendClient(
                    config.lekko_uri,
                    config.owner_name,
                    config.repo_name,
                    MemoryStore(),
                    config.api_key,
                    config.context,
                )
            case _:
                raise exceptions.LekkoError("Unknown client mode")
        return __client


def set_client(client: Client) -> None:
    global __client
    with __client_lock:
        if __client:
            __client.close()
        __client = client


def close() -> None:
    global __client
    with __client_lock:
        if __client:
            __client.close()
            __client = None


TFunc = TypeVar("TFunc", bound=Callable[..., Any])


def __get_safe(func: TFunc) -> TFunc:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with __client_lock:
            if not __client:
                raise exceptions.ClientNotInitialized("lekko_client.initialize() must be called prior to using API")
            return func(*args, **kwargs)

    return cast(TFunc, wrapper)


@__get_safe
def get_bool(namespace: str, key: str, context: Dict[str, Any]) -> bool:
    assert __client
    return __client.get_bool(namespace, key, context)


@__get_safe
def get_int(namespace: str, key: str, context: Dict[str, Any]) -> int:
    assert __client
    return __client.get_int(namespace, key, context)


@__get_safe
def get_float(namespace: str, key: str, context: Dict[str, Any]) -> float:
    assert __client
    return __client.get_float(namespace, key, context)


@__get_safe
def get_string(namespace: str, key: str, context: Dict[str, Any]) -> str:
    assert __client
    return __client.get_string(namespace, key, context)


@__get_safe
def get_json(namespace: str, key: str, context: Dict[str, Any]) -> Any:
    assert __client
    return __client.get_json(namespace, key, context)


@__get_safe
def get_proto(
    namespace: str,
    key: str,
    context: Dict[str, Any],
) -> ProtoMessage:
    assert __client
    return __client.get_proto(namespace, key, context)


@__get_safe
def get_proto_by_type(
    namespace: str,
    key: str,
    context: Dict[str, Any],
    proto_message_type: Type[Client.ProtoType],
) -> Client.ProtoType:
    assert __client
    return __client.get_proto_by_type(namespace, key, context, proto_message_type)
