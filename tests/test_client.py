import json

from grpc import StatusCode

from lekko_client.client import SidecarClient
from lekko_client.gen.lekko.client.v1beta1 import configuration_service_pb2 as messages


def test_get_bool(test_server):
    test_server.mock_async_response("GetBoolValue", messages.GetBoolValueResponse(value=True))

    client = SidecarClient("owner", "repo", "namespace", "lekko_apikey123")
    resp = client.get_bool("val", {})

    assert resp == True


def test_get_int(test_server):
    test_server.mock_async_response("GetIntValue", messages.GetIntValueResponse(value=10))

    client = SidecarClient("owner", "repo", "namespace", "lekko_apikey123")
    resp = client.get_int("val", {})

    assert resp == 10


def test_get_float(test_server):
    test_server.mock_async_response("GetFloatValue", messages.GetFloatValueResponse(value=1.5))

    client = SidecarClient("owner", "repo", "namespace", "lekko_apikey123")
    resp = client.get_float("val", {})

    assert resp == 1.5


def test_get_string(test_server):
    test_server.mock_async_response("GetStringValue", messages.GetStringValueResponse(value="feature value"))

    client = SidecarClient("owner", "repo", "namespace", "lekko_apikey123")
    resp = client.get_string("val", {})

    assert resp == "feature value"


def test_get_json(test_server):
    expected = {"key": "value", "int_key": 1}
    test_server.mock_async_response(
        "GetJSONValue", messages.GetJSONValueResponse(value=bytes(json.dumps(expected), "utf-8"))
    )

    client = SidecarClient("owner", "repo", "namespace", "lekko_apikey123")
    resp = client.get_json("val", {})

    assert resp == expected
