class LekkoError(Exception):
    pass


class AuthenticationError(LekkoError):
    pass


class LekkoRpcError(LekkoError):
    pass


class NamespaceNotFound(LekkoRpcError):
    pass


class ConfigNotFoundError(LekkoRpcError):
    pass


FeatureNotFound = ConfigNotFoundError


class MismatchedType(LekkoRpcError):
    pass


class MismatchedProtoType(LekkoError):
    pass


class EvaluationError(LekkoError):
    pass


class GitRepoNotFound(LekkoError):
    pass


class ClientNotInitialized(LekkoError):
    pass
