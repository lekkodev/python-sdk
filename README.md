[![Coverage Status](https://img.shields.io/codecov/c/github/lekkodev/python-sdk)](https://app.codecov.io/github/lekkodev/python-sdk) [![PyPI version](https://badge.fury.io/py/lekko_client.svg)](https://badge.fury.io/py/lekko_client)

# Lekko Python SDK

The Lekko SDK for Python

## Install

The `lekko_client` package is published on [PyPI](https://pypi.org/project/lekko_client/).

```
pip install lekko_client
```

## Usage

### Initializing a cached Lekko client

Creates a client that fetches configs from Lekko backend and caches them in memory. Configs are kept up to date via polling.

```python
import lekko_client

lekko_client.initialize(lekko_client.CachedServerConfig(
    owner_name="<REPOSITORY_OWNER>",
    repo_name="<REPOSITORY_NAME>",
    api_key="<API_KEY>",  # Optional - defaults to "LEKKO_API_KEY" ENV Var
    lekko_uri="<URI>",    # Optional - defaults to "prod.api.lekko.dev:443"
    context={},           # Optionally provide context dict to be merged into each get request
))

str_config = lekko_client.get_string("my_namespace", "my_config", {"context_key": "context_val"})
```

### Initializing a cached Lekko client in git mode

Creates a client that reads configs from a git repository on disk and caches them in memory. Configs are kept up to date via a file watcher.

```python
import lekko_client

lekko_client.initialize(lekko_client.CachedGitConfig(
    owner_name="<REPOSITORY_OWNER>",
    repo_name="<REPOSITORY_NAME>",
    git_repo_path="<GIT_REPO_PATH>",
    api_key="<API_KEY>",  # Optional - defaults to "LEKKO_API_KEY" ENV Var
    lekko_uri="<URI>",    # Optional - defaults to "prod.api.lekko.dev:443"
    context={},           # Optionally provide context dict to be merged into each get request
))

str_config = lekko_client.get_string("my_namespace", "my_config", {"context_key": "context_val"})
```

### Initializing a Lekko client for remote evaluation

Create a client that communicates with the Lekko API or a Lekko sidecar for remote evaluation

```python
import lekko_client

lekko_client.initialize(lekko_client.APIConfig(  # Or lekko_client.SidecarConfig
    owner_name="<REPOSITORY_OWNER>",
    repo_name="<REPOSITORY_NAME>",
    api_key="<API_KEY>",  # Optional - defaults to "LEKKO_API_KEY" ENV Var
    context={},           # Optionally provide context dict to be merged into each get request
))

str_config = lekko_client.get_string("my_namespace", "my_config", {"context_key": "context_val"})
```

## Lifecycle management

`lekko_client.initialize()` must be invoked prior to calling the `lekko_client.get_*()` functions and should not be called multiple times. We recommend invoking it early in your app's lifecycle, for example when constructing your Flask app or as part of FastAPI's lifecycle context manager.

We recommend you invoke `lekko_client.close()` during app shutdown. This will ensure all evaluation events are properly tracked and the SDK client is deregistered correctly.

It is also possible to do your own lifecycle management and avoid the `lekko_client.initialize()` and `lekko_client.get_*()` methods entirely. The above root module-level methods are provided for convenience to suit most use cases, without having to explicitly manage a client instance and pass it around. Feel free to construct any of the clients in `lekko_client.clients` manually.

For example:

```python
from lekko_client.clients import APIClient

client = APIClient(
    owner_name="<REPOSITORY_OWNER>",
    repo_name="<REPOSITORY_NAME>",
    api_key="<API_KEY>",
)

...

def use_client(client):
    str_config = client.get_string("my_namespace", "my_config", {"context_key": "context_val"})
    return str_config

use_client(client)
```

## Protobuf configs

There are two methods to retrieve protobuf configs, with one allowing you to specify the expected proto message type.

- `get_proto_by_type(key, context, proto_message_type)` will attempt to convert the config to the specified type and raise `MismatchedProtoType` on failure.

- `get_proto(key, context)` will attempt to locate the proto message type in the proto symbol database, which tracks imported proto types. If unable to locate the type, it will simply return the message as a `google.protobuf.any_pb2.Any`

For example, if you have a proto config named `proto_config` defined as:

```
{
  "@type": "type.googleapis.com/google.protobuf.BoolValue",
  "value": false
}
```

You would see the following behavior:

```python
>>> config_value = client.get_proto("proto", {})
>>> type(config_value)
<class 'google.protobuf.any_pb2.Any'>
>>> config_value.value
b''
```

But after importing the appropriate type:

```python
>>> from google.protobuf import wrappers_pb2
>>> config_value = client.get_proto("proto", {})
>>> type(config_value)
<class 'google.protobuf.wrappers_pb2.BoolValue'>
>>> config_value.value
False
```

## Example

See: https://github.com/lekkodev/python-sdk/blob/main/example.py
