from abc import ABC, abstractmethod
from hashlib import sha256

from lekko_client.gen.lekko.backend.v1beta1.distribution_service_pb2 import (
    GetRepositoryContentsResponse,
)
from lekko_client.models import FeatureData


class Store(ABC):
    def __init__(self):
        self._commit_sha = ""
        self._content_hash = ""

    @abstractmethod
    def get(self, namespace: str, config_key: str) -> FeatureData:
        ...

    def load(self, contents: GetRepositoryContentsResponse) -> bool:
        if not contents:
            return False

        contents = self.sort_contents(contents)
        content_hash = self.hash_contents(contents)

        if not self.should_update(contents, content_hash):
            return False

        if not self.load_impl(contents):
            return False

        self._commit_sha = contents.commit_sha
        self._content_hash = content_hash
        return True

    @abstractmethod
    def load_impl(self, contents: GetRepositoryContentsResponse) -> bool:
        ...

    @property
    def commit_sha(self) -> str:
        return self._commit_sha

    @property
    def content_hash(self) -> str:
        return self._content_hash

    def should_update(self, contents: GetRepositoryContentsResponse, content_hash: str):
        return contents.commit_sha != self.commit_sha or content_hash != self.content_hash

    @classmethod
    def sort_contents(cls, contents: GetRepositoryContentsResponse):
        for ns in contents.namespaces:
            ns.features.sort(key=lambda cfg: cfg.name)
        contents.namespaces.sort(key=lambda ns: ns.name)
        return contents

    @classmethod
    def hash_contents(cls, contents: GetRepositoryContentsResponse):
        return sha256(contents.SerializeToString()).hexdigest()
