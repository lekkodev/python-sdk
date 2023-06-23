[![Coverage Status](https://img.shields.io/codecov/c/github/lekkodev/python-sdk)](https://app.codecov.io/github/lekkodev/python-sdk)

# Lekko Python SDK
The Lekko SDK for Python

## Getting Started

### Installation
`pip install lekko_client`

### Initializing a Lekko client
```python
from lekko_client import APIClient, SidecarClient

client = SidecarClient(   # Or APIClient
    owner_name="<REPOSITORY_OWNER>",
    repo_name="<REPOSITORY_NAME>",
    namespace="<NAMESPACE>",
    api_key="<API_KEY>",  # Optional - defaults to "LEKKO_API_KEY" ENV Var
    uri="<URI>",          # Optional - defaults to "localhost:50051" for Sidecar
                          # and "prod.api.lekko.dev:443" for APIClient
    context={},           # Optionally provide context dict to be merged into each get request
)

str_feature = client.get_string("my_feature", {"context_key": "context_val"})
```


## Proto Features
There are two methods to retrieve a Proto Feature, with one allowing you to specify the expected proto message type.

`get_proto_by_type(key, context, proto_message_type)` will attempt to convert the feature to the specified type and raise `MismatchedProtoType` on failure.

`get_proto(key, context)` will attempt to locate the proto message type in the proto symbol database, which tracks imported proto types. If unable to locate the type, it will simply return the message as a `google.protobuf.any_pb2.Any`

For example, if you have a proto feature named `proto_feature` defined as:
```
{
  "@type": "type.googleapis.com/google.protobuf.BoolValue",
  "value": false
}
```
You would see the following behavior:
```python
>>> feature_value = client.get_proto("proto", {})
>>> type(feature_value)
<class 'google.protobuf.any_pb2.Any'>
>>> feature_value.value
b''
```
But after importing the appropriate type:
```python
>>> from google.protobuf import wrappers_pb2
>>> feature_value = client.get_proto("proto", {})
>>> type(feature_value)
<class 'google.protobuf.wrappers_pb2.BoolValue'>
>>> feature_value.value
False
```

## Example
See: https://github.com/lekkodev/python-sdk/blob/main/example.py
