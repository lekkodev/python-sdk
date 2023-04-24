# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import configuration_service_pb2 as lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2


class ConfigurationServiceStub(object):
    """Initial implementation of a feature flagging service.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetBoolValue = channel.unary_unary(
                '/lekko.client.v1beta1.ConfigurationService/GetBoolValue',
                request_serializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetBoolValueRequest.SerializeToString,
                response_deserializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetBoolValueResponse.FromString,
                )
        self.GetIntValue = channel.unary_unary(
                '/lekko.client.v1beta1.ConfigurationService/GetIntValue',
                request_serializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetIntValueRequest.SerializeToString,
                response_deserializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetIntValueResponse.FromString,
                )
        self.GetFloatValue = channel.unary_unary(
                '/lekko.client.v1beta1.ConfigurationService/GetFloatValue',
                request_serializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetFloatValueRequest.SerializeToString,
                response_deserializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetFloatValueResponse.FromString,
                )
        self.GetStringValue = channel.unary_unary(
                '/lekko.client.v1beta1.ConfigurationService/GetStringValue',
                request_serializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetStringValueRequest.SerializeToString,
                response_deserializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetStringValueResponse.FromString,
                )
        self.GetProtoValue = channel.unary_unary(
                '/lekko.client.v1beta1.ConfigurationService/GetProtoValue',
                request_serializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetProtoValueRequest.SerializeToString,
                response_deserializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetProtoValueResponse.FromString,
                )
        self.GetJSONValue = channel.unary_unary(
                '/lekko.client.v1beta1.ConfigurationService/GetJSONValue',
                request_serializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetJSONValueRequest.SerializeToString,
                response_deserializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetJSONValueResponse.FromString,
                )
        self.Register = channel.unary_unary(
                '/lekko.client.v1beta1.ConfigurationService/Register',
                request_serializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.RegisterRequest.SerializeToString,
                response_deserializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.RegisterResponse.FromString,
                )
        self.Deregister = channel.unary_unary(
                '/lekko.client.v1beta1.ConfigurationService/Deregister',
                request_serializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.DeregisterRequest.SerializeToString,
                response_deserializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.DeregisterResponse.FromString,
                )


class ConfigurationServiceServicer(object):
    """Initial implementation of a feature flagging service.
    """

    def GetBoolValue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetIntValue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFloatValue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStringValue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetProtoValue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetJSONValue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Register(self, request, context):
        """Register is used to denote a RepositoryKey and namespaces within it
        that a client is interested in so the server can cache and keep up to date.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Deregister(self, request, context):
        """Deregister is used to tell the server that a client is shutting down. It is not
        required but preferable to have implementations call this once their lifecycle
        has completed.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ConfigurationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetBoolValue': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBoolValue,
                    request_deserializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetBoolValueRequest.FromString,
                    response_serializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetBoolValueResponse.SerializeToString,
            ),
            'GetIntValue': grpc.unary_unary_rpc_method_handler(
                    servicer.GetIntValue,
                    request_deserializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetIntValueRequest.FromString,
                    response_serializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetIntValueResponse.SerializeToString,
            ),
            'GetFloatValue': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFloatValue,
                    request_deserializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetFloatValueRequest.FromString,
                    response_serializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetFloatValueResponse.SerializeToString,
            ),
            'GetStringValue': grpc.unary_unary_rpc_method_handler(
                    servicer.GetStringValue,
                    request_deserializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetStringValueRequest.FromString,
                    response_serializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetStringValueResponse.SerializeToString,
            ),
            'GetProtoValue': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProtoValue,
                    request_deserializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetProtoValueRequest.FromString,
                    response_serializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetProtoValueResponse.SerializeToString,
            ),
            'GetJSONValue': grpc.unary_unary_rpc_method_handler(
                    servicer.GetJSONValue,
                    request_deserializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetJSONValueRequest.FromString,
                    response_serializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetJSONValueResponse.SerializeToString,
            ),
            'Register': grpc.unary_unary_rpc_method_handler(
                    servicer.Register,
                    request_deserializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.RegisterRequest.FromString,
                    response_serializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.RegisterResponse.SerializeToString,
            ),
            'Deregister': grpc.unary_unary_rpc_method_handler(
                    servicer.Deregister,
                    request_deserializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.DeregisterRequest.FromString,
                    response_serializer=lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.DeregisterResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'lekko.client.v1beta1.ConfigurationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ConfigurationService(object):
    """Initial implementation of a feature flagging service.
    """

    @staticmethod
    def GetBoolValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lekko.client.v1beta1.ConfigurationService/GetBoolValue',
            lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetBoolValueRequest.SerializeToString,
            lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetBoolValueResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetIntValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lekko.client.v1beta1.ConfigurationService/GetIntValue',
            lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetIntValueRequest.SerializeToString,
            lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetIntValueResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFloatValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lekko.client.v1beta1.ConfigurationService/GetFloatValue',
            lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetFloatValueRequest.SerializeToString,
            lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetFloatValueResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetStringValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lekko.client.v1beta1.ConfigurationService/GetStringValue',
            lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetStringValueRequest.SerializeToString,
            lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetStringValueResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetProtoValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lekko.client.v1beta1.ConfigurationService/GetProtoValue',
            lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetProtoValueRequest.SerializeToString,
            lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetProtoValueResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetJSONValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lekko.client.v1beta1.ConfigurationService/GetJSONValue',
            lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetJSONValueRequest.SerializeToString,
            lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.GetJSONValueResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lekko.client.v1beta1.ConfigurationService/Register',
            lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.RegisterRequest.SerializeToString,
            lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.RegisterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Deregister(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lekko.client.v1beta1.ConfigurationService/Deregister',
            lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.DeregisterRequest.SerializeToString,
            lekko_dot_client_dot_v1beta1_dot_configuration__service__pb2.DeregisterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)