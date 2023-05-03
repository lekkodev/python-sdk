import json

from lekko_client.client import SidecarClient
from lekko_client.gen.lekko.client.v1beta1 import configuration_service_pb2 as messages


def test_get_bool(test_server):
    requests = [
        test_server.MockRequestResponse("Register", messages.RegisterResponse),
        test_server.MockRequestResponse("GetBoolValue", messages.GetBoolValueResponse(value=True)),
    ]

    test_server.mock_async_responses(requests)

    client = SidecarClient("owner", "repo", "namespace", "lekko_apikey123")
    resp = client.get_bool("val", {})

    assert resp is True


def test_get_int(test_server):
    requests = [
        test_server.MockRequestResponse("Register", messages.RegisterResponse),
        test_server.MockRequestResponse("GetIntValue", messages.GetIntValueResponse(value=10)),
    ]

    test_server.mock_async_responses(requests)

    client = SidecarClient("owner", "repo", "namespace", "lekko_apikey123")
    resp = client.get_int("val", {})

    assert resp == 10


def test_get_float(test_server):
    requests = [
        test_server.MockRequestResponse("Register", messages.RegisterResponse),
        test_server.MockRequestResponse("GetFloatValue", messages.GetFloatValueResponse(value=1.5)),
    ]

    test_server.mock_async_responses(requests)

    client = SidecarClient("owner", "repo", "namespace", "lekko_apikey123")
    resp = client.get_float("val", {})

    assert resp == 1.5


def test_get_string(test_server):
    requests = [
        test_server.MockRequestResponse("Register", messages.RegisterResponse),
        test_server.MockRequestResponse("GetStringValue", messages.GetStringValueResponse(value="feature value")),
    ]
    test_server.mock_async_responses(requests)

    client = SidecarClient("owner", "repo", "namespace", "lekko_apikey123")
    resp = client.get_string("val", {})

    assert resp == "feature value"


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
