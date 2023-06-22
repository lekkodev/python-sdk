import json
import os
from unittest import mock

import grpc
import pytest
from google.protobuf import wrappers_pb2
from google.protobuf.any_pb2 import Any

from lekko_client.client import (
    APIClient,
    AuthenticationError,
    FeatureNotFound,
    MismatchedProtoType,
    MismatchedType,
    SidecarClient,
)
from lekko_client.gen.lekko.client.v1beta1 import configuration_service_pb2 as messages


@pytest.mark.parametrize(
    "proto_fn_name,response_obj,response_val,test_fn_name",
    [
        ("GetBoolValue", messages.GetBoolValueResponse, True, "get_bool"),
        ("GetIntValue", messages.GetIntValueResponse, 10, "get_int"),
        ("GetFloatValue", messages.GetFloatValueResponse, 2.5, "get_float"),
        ("GetStringValue", messages.GetStringValueResponse, "test string", "get_string"),
    ],
)
def test_get_scalar(test_server, proto_fn_name, response_obj, response_val, test_fn_name):
    requests = [
        test_server.MockRequestResponse("Register", messages.RegisterResponse),
        test_server.MockRequestResponse(proto_fn_name, response_obj(value=response_val)),
    ]

    async_requests = test_server.mock_async_responses(requests)

    owner_name = "owner"
    repo_name = "repo"
    namespace = "namespace"
    feature_name = "val"
    api_key = "lekko_apikey123"
    context = {"ctx_key": response_val}

    client = SidecarClient(owner_name, repo_name, namespace, api_key)
    resp = getattr(client, test_fn_name)(feature_name, context)

    assert resp == response_val
    completed_requests = async_requests.result()
    assert len(completed_requests) == 2
    assert completed_requests[0].arg.repo_key.owner_name == owner_name
    assert completed_requests[0].arg.repo_key.repo_name == repo_name
    assert completed_requests[0].arg.namespace_list == [namespace]
    assert ("apikey", api_key) in completed_requests[0].metadata
    assert completed_requests[1].arg.key == feature_name
    req_ctx = {k: getattr(v, v.WhichOneof("kind")) for k, v in completed_requests[1].arg.context.items()}
    assert req_ctx == context
    assert ("apikey", api_key) in completed_requests[1].metadata


def test_get_json(test_server):
    expected = {"key": "value", "int_key": 1}
    requests = [
        test_server.MockRequestResponse("Register", messages.RegisterResponse),
        test_server.MockRequestResponse(
            "GetJSONValue", messages.GetJSONValueResponse(value=bytes(json.dumps(expected), "utf-8"))
        ),
    ]
    test_server.mock_async_responses(requests)

    client = SidecarClient("owner", "repo", "namespace", "lekko_apikey123")
    resp = client.get_json("val", {})

    assert resp == expected


def test_get_proto_by_type(test_server):
    any_proto = Any()
    int_proto = wrappers_pb2.Int32Value(value=10)
    any_proto.Pack(int_proto)
    requests = [
        test_server.MockRequestResponse("Register", messages.RegisterResponse),
        test_server.MockRequestResponse("GetProtoValue", messages.GetProtoValueResponse(value=any_proto)),
        test_server.MockRequestResponse("GetProtoValue", messages.GetProtoValueResponse(value=any_proto)),
    ]
    test_server.mock_async_responses(requests)

    client = SidecarClient("owner", "repo", "namespace", "lekko_apikey123")
    resp = client.get_proto_by_type("val", {}, wrappers_pb2.Int32Value)

    assert resp == int_proto

    with pytest.raises(MismatchedProtoType):
        client.get_proto_by_type("val", {}, wrappers_pb2.Int64Value)


def test_get_proto(test_server):
    any_proto = Any()
    int_proto = wrappers_pb2.Int32Value(value=10)
    any_proto.Pack(int_proto)
    lekko_any_proto = messages.Any(type_url=any_proto.type_url, value=any_proto.value)
    requests = [
        test_server.MockRequestResponse("Register", messages.RegisterResponse),
        test_server.MockRequestResponse("GetProtoValue", messages.GetProtoValueResponse(value=any_proto)),
        test_server.MockRequestResponse("GetProtoValue", messages.GetProtoValueResponse(value=any_proto)),
        test_server.MockRequestResponse(
            "GetProtoValue", messages.GetProtoValueResponse(value=any_proto, value_v2=lekko_any_proto)
        ),
        test_server.MockRequestResponse("GetProtoValue", messages.GetProtoValueResponse(value_v2=lekko_any_proto)),
    ]
    test_server.mock_async_responses(requests)

    client = SidecarClient("owner", "repo", "namespace", "lekko_apikey123")

    # When the proto symbol is loaded in the db, it should Unpack correctly
    resp = client.get_proto("val", {})
    assert resp == int_proto

    # If the proto symbol can't be found, we fall through to returning the Any proto
    with mock.patch("google.protobuf.symbol_database.SymbolDatabase.GetSymbol", side_effect=KeyError):
        resp = client.get_proto("val", {})
        assert resp == any_proto

    # test get proto with value and value_v2 being returned
    resp = client.get_proto("val", {})
    assert resp == int_proto

    # test get proto with only value_v2 being returned
    resp = client.get_proto("val", {})
    assert resp == int_proto


def test_missing_api_key(test_server):
    expected = True
    requests = [
        test_server.MockRequestResponse("Register", messages.RegisterResponse),
        test_server.MockRequestResponse("GetBoolValue", messages.GetBoolValueResponse(value=expected)),
    ]
    test_server.mock_async_responses(requests)

    with pytest.raises(AuthenticationError):
        SidecarClient("owner", "repo", "namespace")

    os.environ["LEKKO_API_KEY"] = "lekko_apikey123"
    client = SidecarClient("owner", "repo", "namespace")
    result = client.get_bool("key", {})
    assert result == expected


# Interceptor can't handle returning errors for some reason
def test_errors(test_server_no_interceptor):
    requests = [
        test_server_no_interceptor.MockRequestResponse("Register", messages.RegisterResponse),
        test_server_no_interceptor.MockRequestResponse(
            fn_name="GetBoolValue",
            response=None,
            status_code=grpc.StatusCode.NOT_FOUND,
            error_text="get evaluable feature: first feature: record not found",
        ),
        test_server_no_interceptor.MockRequestResponse(
            "GetBoolValue",
            None,
            grpc.StatusCode.INVALID_ARGUMENT,
            "requested feature is not of type bool",
        ),
    ]

    test_server_no_interceptor.mock_async_responses(requests)

    client = SidecarClient("owner", "repo", "namespace", "lekko_apikey123")
    with pytest.raises(FeatureNotFound):
        client.get_bool("key", {})

    with pytest.raises(MismatchedType):
        client.get_bool("key", {})


def test_proto_errors(test_server_no_interceptor):
    requests = [
        test_server_no_interceptor.MockRequestResponse("Register", messages.RegisterResponse),
        test_server_no_interceptor.MockRequestResponse(
            fn_name="GetProtoValue",
            response=None,
            status_code=grpc.StatusCode.NOT_FOUND,
            error_text="get evaluable feature: first feature: record not found",
        ),
        test_server_no_interceptor.MockRequestResponse(
            "GetProtoValue",
            None,
            grpc.StatusCode.INVALID_ARGUMENT,
            "requested feature is not of type proto",
        ),
        test_server_no_interceptor.MockRequestResponse(
            "GetProtoValue",
            None,
            grpc.StatusCode.INTERNAL,
            "internal server error",
        ),
    ]

    test_server_no_interceptor.mock_async_responses(requests)

    client = SidecarClient("owner", "repo", "namespace", "lekko_apikey123")
    with pytest.raises(FeatureNotFound):
        client.get_proto("key", {})

    with pytest.raises(MismatchedType):
        client.get_proto("key", {})

    with pytest.raises(grpc.RpcError):
        client.get_proto("key", {})


def test_get_api_client(test_server):
    requests = [
        test_server.MockRequestResponse("Register", messages.RegisterResponse),
        test_server.MockRequestResponse("GetStringValue", messages.GetStringValueResponse(value="feature value")),
    ]
    test_server.mock_async_responses(requests)

    client = APIClient("owner", "repo", "namespace", "lekko_apikey123")
    resp = client.get_string("val", {"conext": "hello"})

    assert resp == "feature value"
