import grpc

from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2 import (
    GetBoolValueResponse,
    GetFloatValueResponse,
    GetIntValueResponse,
    GetJSONValueResponse,
    GetProtoValueResponse,
    GetStringValueResponse,
    RegisterResponse,
)
from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2_grpc import (
    ConfigurationServiceServicer,
)


class MockConfigurationService(ConfigurationServiceServicer):
    RESPONSES = {
        "bool_val": True,
        "int_val": 10,
        "float_val": 25.5,
        "string_val": "hello world",
        "json_val": {"key": "value"},
    }

    def _get(self, request, context, expected_type, resp_type):
        val = self.RESPONSES.get(request.key)
        if not val:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("not found")
            return resp_type()
        elif not isinstance(val, expected_type):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("type mismatch")
            return resp_type()

        return resp_type(value=val)

    def GetBoolValue(self, request, context):
        return self._get(request, context, bool, GetBoolValueResponse)

    def GetIntValue(self, request, context):
        return self._get(request, context, int, GetIntValueResponse)

    def GetFloatValue(self, request, context):
        return self._get(request, context, float, GetFloatValueResponse)

    def GetStringValue(self, request, context):
        return self._get(request, context, str, GetStringValueResponse)

    def GetProtoValue(self, request, context):
        return GetProtoValueResponse()

    def GetJSONValue(self, request, context):
        return self._get(request, context, dict, GetJSONValueResponse)

    def Register(self, request, context):
        return RegisterResponse()
