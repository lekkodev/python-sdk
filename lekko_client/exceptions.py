from grpc import RpcError


class LekkoError(Exception):
    pass


class AuthenticationError(LekkoError):
    pass


class LekkoRpcError(LekkoError):
    pass


class FeatureNotFound(LekkoRpcError):
    pass


class MismatchedType(LekkoRpcError):
    pass
