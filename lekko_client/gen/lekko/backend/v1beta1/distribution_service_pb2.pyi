"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright 2022 Lekko Technologies, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import google.protobuf.timestamp_pb2
import lekko_client.gen.lekko.feature.v1beta1.feature_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class RepositoryKey(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OWNER_NAME_FIELD_NUMBER: builtins.int
    REPO_NAME_FIELD_NUMBER: builtins.int
    owner_name: builtins.str
    repo_name: builtins.str
    def __init__(
        self,
        *,
        owner_name: builtins.str = ...,
        repo_name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["owner_name", b"owner_name", "repo_name", b"repo_name"]) -> None: ...

global___RepositoryKey = RepositoryKey

@typing_extensions.final
class GetRepositoryVersionRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    REPO_KEY_FIELD_NUMBER: builtins.int
    SESSION_KEY_FIELD_NUMBER: builtins.int
    @property
    def repo_key(self) -> global___RepositoryKey: ...
    session_key: builtins.str
    def __init__(
        self,
        *,
        repo_key: global___RepositoryKey | None = ...,
        session_key: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["repo_key", b"repo_key"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["repo_key", b"repo_key", "session_key", b"session_key"]) -> None: ...

global___GetRepositoryVersionRequest = GetRepositoryVersionRequest

@typing_extensions.final
class GetRepositoryVersionResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COMMIT_SHA_FIELD_NUMBER: builtins.int
    commit_sha: builtins.str
    def __init__(
        self,
        *,
        commit_sha: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["commit_sha", b"commit_sha"]) -> None: ...

global___GetRepositoryVersionResponse = GetRepositoryVersionResponse

@typing_extensions.final
class GetRepositoryContentsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    REPO_KEY_FIELD_NUMBER: builtins.int
    NAMESPACE_NAME_FIELD_NUMBER: builtins.int
    FEATURE_NAME_FIELD_NUMBER: builtins.int
    SESSION_KEY_FIELD_NUMBER: builtins.int
    @property
    def repo_key(self) -> global___RepositoryKey: ...
    namespace_name: builtins.str
    """optional namespace_name to filter responses by"""
    feature_name: builtins.str
    """optional feature_name to filter responses by"""
    session_key: builtins.str
    def __init__(
        self,
        *,
        repo_key: global___RepositoryKey | None = ...,
        namespace_name: builtins.str = ...,
        feature_name: builtins.str = ...,
        session_key: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["repo_key", b"repo_key"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["feature_name", b"feature_name", "namespace_name", b"namespace_name", "repo_key", b"repo_key", "session_key", b"session_key"]) -> None: ...

global___GetRepositoryContentsRequest = GetRepositoryContentsRequest

@typing_extensions.final
class GetRepositoryContentsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COMMIT_SHA_FIELD_NUMBER: builtins.int
    NAMESPACES_FIELD_NUMBER: builtins.int
    commit_sha: builtins.str
    @property
    def namespaces(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Namespace]: ...
    def __init__(
        self,
        *,
        commit_sha: builtins.str = ...,
        namespaces: collections.abc.Iterable[global___Namespace] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["commit_sha", b"commit_sha", "namespaces", b"namespaces"]) -> None: ...

global___GetRepositoryContentsResponse = GetRepositoryContentsResponse

@typing_extensions.final
class Namespace(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    FEATURES_FIELD_NUMBER: builtins.int
    name: builtins.str
    @property
    def features(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Feature]: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        features: collections.abc.Iterable[global___Feature] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["features", b"features", "name", b"name"]) -> None: ...

global___Namespace = Namespace

@typing_extensions.final
class Feature(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    SHA_FIELD_NUMBER: builtins.int
    FEATURE_FIELD_NUMBER: builtins.int
    name: builtins.str
    sha: builtins.str
    """The sha of the protobuf binary according to git."""
    @property
    def feature(self) -> lekko_client.gen.lekko.feature.v1beta1.feature_pb2.Feature: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        sha: builtins.str = ...,
        feature: lekko_client.gen.lekko.feature.v1beta1.feature_pb2.Feature | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["feature", b"feature"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["feature", b"feature", "name", b"name", "sha", b"sha"]) -> None: ...

global___Feature = Feature

@typing_extensions.final
class ContextKey(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KEY_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    key: builtins.str
    type: builtins.str
    def __init__(
        self,
        *,
        key: builtins.str = ...,
        type: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "type", b"type"]) -> None: ...

global___ContextKey = ContextKey

@typing_extensions.final
class FlagEvaluationEvent(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    REPO_KEY_FIELD_NUMBER: builtins.int
    COMMIT_SHA_FIELD_NUMBER: builtins.int
    FEATURE_SHA_FIELD_NUMBER: builtins.int
    NAMESPACE_NAME_FIELD_NUMBER: builtins.int
    FEATURE_NAME_FIELD_NUMBER: builtins.int
    CONTEXT_KEYS_FIELD_NUMBER: builtins.int
    RESULT_PATH_FIELD_NUMBER: builtins.int
    CLIENT_EVENT_TIME_FIELD_NUMBER: builtins.int
    @property
    def repo_key(self) -> global___RepositoryKey: ...
    commit_sha: builtins.str
    feature_sha: builtins.str
    namespace_name: builtins.str
    feature_name: builtins.str
    @property
    def context_keys(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ContextKey]:
        """A list of context keys (not values) that were provided at runtime."""
    @property
    def result_path(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]:
        """The node in the tree that contained the final return value of the feature."""
    @property
    def client_event_time(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    def __init__(
        self,
        *,
        repo_key: global___RepositoryKey | None = ...,
        commit_sha: builtins.str = ...,
        feature_sha: builtins.str = ...,
        namespace_name: builtins.str = ...,
        feature_name: builtins.str = ...,
        context_keys: collections.abc.Iterable[global___ContextKey] | None = ...,
        result_path: collections.abc.Iterable[builtins.int] | None = ...,
        client_event_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["client_event_time", b"client_event_time", "repo_key", b"repo_key"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["client_event_time", b"client_event_time", "commit_sha", b"commit_sha", "context_keys", b"context_keys", "feature_name", b"feature_name", "feature_sha", b"feature_sha", "namespace_name", b"namespace_name", "repo_key", b"repo_key", "result_path", b"result_path"]) -> None: ...

global___FlagEvaluationEvent = FlagEvaluationEvent

@typing_extensions.final
class SendFlagEvaluationMetricsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    EVENTS_FIELD_NUMBER: builtins.int
    SESSION_KEY_FIELD_NUMBER: builtins.int
    @property
    def events(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___FlagEvaluationEvent]: ...
    session_key: builtins.str
    def __init__(
        self,
        *,
        events: collections.abc.Iterable[global___FlagEvaluationEvent] | None = ...,
        session_key: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["events", b"events", "session_key", b"session_key"]) -> None: ...

global___SendFlagEvaluationMetricsRequest = SendFlagEvaluationMetricsRequest

@typing_extensions.final
class SendFlagEvaluationMetricsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___SendFlagEvaluationMetricsResponse = SendFlagEvaluationMetricsResponse

@typing_extensions.final
class RegisterClientRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    REPO_KEY_FIELD_NUMBER: builtins.int
    NAMESPACE_LIST_FIELD_NUMBER: builtins.int
    INITIAL_BOOTSTRAP_SHA_FIELD_NUMBER: builtins.int
    SIDECAR_VERSION_FIELD_NUMBER: builtins.int
    @property
    def repo_key(self) -> global___RepositoryKey: ...
    @property
    def namespace_list(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """The namespaces to register within the repo. If empty,
        all namespaces will be registered.
        """
    initial_bootstrap_sha: builtins.str
    """If the client was initialized from a git bootstrap,
    the commit sha is provided. If there was no bootstrap, this
    can be an empty string.
    """
    sidecar_version: builtins.str
    """If the client is a lekko sidecar, provide the semver version,
    or if not available, the sha of the sidecar.
    """
    def __init__(
        self,
        *,
        repo_key: global___RepositoryKey | None = ...,
        namespace_list: collections.abc.Iterable[builtins.str] | None = ...,
        initial_bootstrap_sha: builtins.str = ...,
        sidecar_version: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["repo_key", b"repo_key"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["initial_bootstrap_sha", b"initial_bootstrap_sha", "namespace_list", b"namespace_list", "repo_key", b"repo_key", "sidecar_version", b"sidecar_version"]) -> None: ...

global___RegisterClientRequest = RegisterClientRequest

@typing_extensions.final
class RegisterClientResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSION_KEY_FIELD_NUMBER: builtins.int
    session_key: builtins.str
    """TODO make this field 1 if we rewrite the API."""
    def __init__(
        self,
        *,
        session_key: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["session_key", b"session_key"]) -> None: ...

global___RegisterClientResponse = RegisterClientResponse

@typing_extensions.final
class DeregisterClientRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SESSION_KEY_FIELD_NUMBER: builtins.int
    session_key: builtins.str
    def __init__(
        self,
        *,
        session_key: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["session_key", b"session_key"]) -> None: ...

global___DeregisterClientRequest = DeregisterClientRequest

@typing_extensions.final
class DeregisterClientResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___DeregisterClientResponse = DeregisterClientResponse

@typing_extensions.final
class GetDeveloperAccessTokenRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___GetDeveloperAccessTokenRequest = GetDeveloperAccessTokenRequest

@typing_extensions.final
class GetDeveloperAccessTokenResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TOKEN_FIELD_NUMBER: builtins.int
    token: builtins.str
    """github access token"""
    def __init__(
        self,
        *,
        token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["token", b"token"]) -> None: ...

global___GetDeveloperAccessTokenResponse = GetDeveloperAccessTokenResponse
