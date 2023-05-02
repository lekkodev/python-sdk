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
import google.protobuf.any_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
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
class GetBoolValueRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class ContextEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___Value: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___Value | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    KEY_FIELD_NUMBER: builtins.int
    CONTEXT_FIELD_NUMBER: builtins.int
    NAMESPACE_FIELD_NUMBER: builtins.int
    REPO_KEY_FIELD_NUMBER: builtins.int
    key: builtins.str
    @property
    def context(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___Value]: ...
    namespace: builtins.str
    @property
    def repo_key(self) -> global___RepositoryKey: ...
    def __init__(
        self,
        *,
        key: builtins.str = ...,
        context: collections.abc.Mapping[builtins.str, global___Value] | None = ...,
        namespace: builtins.str = ...,
        repo_key: global___RepositoryKey | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["repo_key", b"repo_key"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["context", b"context", "key", b"key", "namespace", b"namespace", "repo_key", b"repo_key"]) -> None: ...

global___GetBoolValueRequest = GetBoolValueRequest

@typing_extensions.final
class GetBoolValueResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUE_FIELD_NUMBER: builtins.int
    value: builtins.bool
    def __init__(
        self,
        *,
        value: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["value", b"value"]) -> None: ...

global___GetBoolValueResponse = GetBoolValueResponse

@typing_extensions.final
class GetIntValueRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class ContextEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___Value: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___Value | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    KEY_FIELD_NUMBER: builtins.int
    CONTEXT_FIELD_NUMBER: builtins.int
    NAMESPACE_FIELD_NUMBER: builtins.int
    REPO_KEY_FIELD_NUMBER: builtins.int
    key: builtins.str
    @property
    def context(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___Value]: ...
    namespace: builtins.str
    @property
    def repo_key(self) -> global___RepositoryKey: ...
    def __init__(
        self,
        *,
        key: builtins.str = ...,
        context: collections.abc.Mapping[builtins.str, global___Value] | None = ...,
        namespace: builtins.str = ...,
        repo_key: global___RepositoryKey | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["repo_key", b"repo_key"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["context", b"context", "key", b"key", "namespace", b"namespace", "repo_key", b"repo_key"]) -> None: ...

global___GetIntValueRequest = GetIntValueRequest

@typing_extensions.final
class GetIntValueResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUE_FIELD_NUMBER: builtins.int
    value: builtins.int
    def __init__(
        self,
        *,
        value: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["value", b"value"]) -> None: ...

global___GetIntValueResponse = GetIntValueResponse

@typing_extensions.final
class GetFloatValueRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class ContextEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___Value: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___Value | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    KEY_FIELD_NUMBER: builtins.int
    CONTEXT_FIELD_NUMBER: builtins.int
    NAMESPACE_FIELD_NUMBER: builtins.int
    REPO_KEY_FIELD_NUMBER: builtins.int
    key: builtins.str
    @property
    def context(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___Value]: ...
    namespace: builtins.str
    @property
    def repo_key(self) -> global___RepositoryKey: ...
    def __init__(
        self,
        *,
        key: builtins.str = ...,
        context: collections.abc.Mapping[builtins.str, global___Value] | None = ...,
        namespace: builtins.str = ...,
        repo_key: global___RepositoryKey | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["repo_key", b"repo_key"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["context", b"context", "key", b"key", "namespace", b"namespace", "repo_key", b"repo_key"]) -> None: ...

global___GetFloatValueRequest = GetFloatValueRequest

@typing_extensions.final
class GetFloatValueResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUE_FIELD_NUMBER: builtins.int
    value: builtins.float
    def __init__(
        self,
        *,
        value: builtins.float = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["value", b"value"]) -> None: ...

global___GetFloatValueResponse = GetFloatValueResponse

@typing_extensions.final
class GetStringValueRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class ContextEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___Value: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___Value | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    KEY_FIELD_NUMBER: builtins.int
    CONTEXT_FIELD_NUMBER: builtins.int
    NAMESPACE_FIELD_NUMBER: builtins.int
    REPO_KEY_FIELD_NUMBER: builtins.int
    key: builtins.str
    @property
    def context(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___Value]: ...
    namespace: builtins.str
    @property
    def repo_key(self) -> global___RepositoryKey: ...
    def __init__(
        self,
        *,
        key: builtins.str = ...,
        context: collections.abc.Mapping[builtins.str, global___Value] | None = ...,
        namespace: builtins.str = ...,
        repo_key: global___RepositoryKey | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["repo_key", b"repo_key"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["context", b"context", "key", b"key", "namespace", b"namespace", "repo_key", b"repo_key"]) -> None: ...

global___GetStringValueRequest = GetStringValueRequest

@typing_extensions.final
class GetStringValueResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUE_FIELD_NUMBER: builtins.int
    value: builtins.str
    def __init__(
        self,
        *,
        value: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["value", b"value"]) -> None: ...

global___GetStringValueResponse = GetStringValueResponse

@typing_extensions.final
class GetProtoValueRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class ContextEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___Value: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___Value | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    KEY_FIELD_NUMBER: builtins.int
    CONTEXT_FIELD_NUMBER: builtins.int
    NAMESPACE_FIELD_NUMBER: builtins.int
    REPO_KEY_FIELD_NUMBER: builtins.int
    key: builtins.str
    @property
    def context(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___Value]: ...
    namespace: builtins.str
    @property
    def repo_key(self) -> global___RepositoryKey: ...
    def __init__(
        self,
        *,
        key: builtins.str = ...,
        context: collections.abc.Mapping[builtins.str, global___Value] | None = ...,
        namespace: builtins.str = ...,
        repo_key: global___RepositoryKey | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["repo_key", b"repo_key"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["context", b"context", "key", b"key", "namespace", b"namespace", "repo_key", b"repo_key"]) -> None: ...

global___GetProtoValueRequest = GetProtoValueRequest

@typing_extensions.final
class GetProtoValueResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUE_FIELD_NUMBER: builtins.int
    @property
    def value(self) -> google.protobuf.any_pb2.Any: ...
    def __init__(
        self,
        *,
        value: google.protobuf.any_pb2.Any | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["value", b"value"]) -> None: ...

global___GetProtoValueResponse = GetProtoValueResponse

@typing_extensions.final
class GetJSONValueRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class ContextEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___Value: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___Value | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    KEY_FIELD_NUMBER: builtins.int
    CONTEXT_FIELD_NUMBER: builtins.int
    NAMESPACE_FIELD_NUMBER: builtins.int
    REPO_KEY_FIELD_NUMBER: builtins.int
    key: builtins.str
    @property
    def context(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___Value]: ...
    namespace: builtins.str
    @property
    def repo_key(self) -> global___RepositoryKey: ...
    def __init__(
        self,
        *,
        key: builtins.str = ...,
        context: collections.abc.Mapping[builtins.str, global___Value] | None = ...,
        namespace: builtins.str = ...,
        repo_key: global___RepositoryKey | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["repo_key", b"repo_key"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["context", b"context", "key", b"key", "namespace", b"namespace", "repo_key", b"repo_key"]) -> None: ...

global___GetJSONValueRequest = GetJSONValueRequest

@typing_extensions.final
class GetJSONValueResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUE_FIELD_NUMBER: builtins.int
    value: builtins.bytes
    def __init__(
        self,
        *,
        value: builtins.bytes = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["value", b"value"]) -> None: ...

global___GetJSONValueResponse = GetJSONValueResponse

@typing_extensions.final
class Value(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    BOOL_VALUE_FIELD_NUMBER: builtins.int
    INT_VALUE_FIELD_NUMBER: builtins.int
    DOUBLE_VALUE_FIELD_NUMBER: builtins.int
    STRING_VALUE_FIELD_NUMBER: builtins.int
    bool_value: builtins.bool
    int_value: builtins.int
    double_value: builtins.float
    string_value: builtins.str
    def __init__(
        self,
        *,
        bool_value: builtins.bool = ...,
        int_value: builtins.int = ...,
        double_value: builtins.float = ...,
        string_value: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["bool_value", b"bool_value", "double_value", b"double_value", "int_value", b"int_value", "kind", b"kind", "string_value", b"string_value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["bool_value", b"bool_value", "double_value", b"double_value", "int_value", b"int_value", "kind", b"kind", "string_value", b"string_value"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["kind", b"kind"]) -> typing_extensions.Literal["bool_value", "int_value", "double_value", "string_value"] | None: ...

global___Value = Value

@typing_extensions.final
class RegisterRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    REPO_KEY_FIELD_NUMBER: builtins.int
    NAMESPACE_LIST_FIELD_NUMBER: builtins.int
    @property
    def repo_key(self) -> global___RepositoryKey: ...
    @property
    def namespace_list(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """The namespaces to register within the repo. If empty,
        all namespaces will be registered.
        """
    def __init__(
        self,
        *,
        repo_key: global___RepositoryKey | None = ...,
        namespace_list: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["repo_key", b"repo_key"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["namespace_list", b"namespace_list", "repo_key", b"repo_key"]) -> None: ...

global___RegisterRequest = RegisterRequest

@typing_extensions.final
class RegisterResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___RegisterResponse = RegisterResponse

@typing_extensions.final
class DeregisterRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___DeregisterRequest = DeregisterRequest

@typing_extensions.final
class DeregisterResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___DeregisterResponse = DeregisterResponse
