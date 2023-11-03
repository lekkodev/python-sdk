"""Lekko Python SDK Client"""

import functools
from dataclasses import dataclass
from threading import RLock
from typing import Any, Dict, Optional, Type

from google.protobuf.message import Message as ProtoMessage

from lekko_client import exceptions
from lekko_client.clients import (
    CachedBackendClient,
    CachedGitClient,
    Client,
    ConfigServiceClient,
)
from lekko_client.constants import LEKKO_API_URL, LEKKO_SIDECAR_URL  # noqa
from lekko_client.stores import MemoryStore

__version__ = "0.1.4"

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
    bootstrap_git_repo_path: Optional[str] = None


@dataclass(kw_only=True)
class CachedGitConfig(Config):
    git_repo_path: str
    local: bool = False


def initialize(config: Config) -> Client:
    global __client
    with __client_lock:
        if __client:
            __client.close()
        match config:
            case APIConfig() | SidecarConfig():
                __client = ConfigServiceClient(
                    config.lekko_uri,
                    config.owner_name,
                    config.repo_name,
                    config.api_key,
                    config.context,
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
                    local=config.local,
                )
            case CachedServerConfig():
                bootstrap_client = (
                    CachedGitClient(
                        config.lekko_uri,
                        config.owner_name,
                        config.repo_name,
                        MemoryStore(),
                        config.bootstrap_git_repo_path,
                        config.api_key,
                        local=True,
                    )
                    if config.bootstrap_git_repo_path
                    else None
                )
                __client = CachedBackendClient(
                    config.lekko_uri,
                    config.owner_name,
                    config.repo_name,
                    MemoryStore(),
                    config.api_key,
                    config.context,
                    bootstrap_client=bootstrap_client,
                )
            case _:
                raise exceptions.LekkoError("Unknown client mode")
        __client.initialize()
        return __client


def set_client(client: Client):
    global __client
    with __client_lock:
        if __client:
            __client.close()
        __client = client


def close():
    global __client
    with __client_lock:
        if __client:
            __client.close()
            __client = None


def __get_safe(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with __client_lock:
            if not __client:
                raise exceptions.ClientNotInitialized(
                    "lekko_client.initialize() must be called prior to using API"
                )
            return func(*args, **kwargs)

    return wrapper


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
def get_json(namespace: str, key: str, context: Dict[str, Any]) -> dict:
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
