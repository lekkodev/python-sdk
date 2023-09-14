import time
from threading import Thread
from typing import Any, Dict, Optional

import grpc

from lekko_client.clients.distribution_client import CachedDistributionClient
from lekko_client.gen.lekko.backend.v1beta1.distribution_service_pb2 import (
    GetRepositoryContentsRequest,
    GetRepositoryContentsResponse,
    GetRepositoryVersionRequest,
)
from lekko_client.stores.store import Store


class CachedBackendClient(CachedDistributionClient):
    class RefreshThread(Thread):
        def __init__(self, client: "CachedBackendClient", refresh_interval_ms: int):
            super().__init__()
            self.daemon = True
            self.client = client
            self.refresh_interval = refresh_interval_ms
            self._enabled = True

        def stop(self):
            self._enabled = False

        def run(self):
            while self._enabled:
                if self.client.should_update_store():
                    self.client.update_store()
                time.sleep(self.refresh_interval / 1000)

    def __init__(
        self,
        uri: str,
        owner_name: str,
        repo_name: str,
        store: Store,
        api_key: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        credentials: grpc.ChannelCredentials = grpc.ssl_channel_credentials(),
    ):
        self.timeout = None
        self.closed = False
        self.update_interval_ms = 1000
        super().__init__(uri, owner_name, repo_name, store, api_key, context, credentials)

    def initialize(self):
        self.update_store()
        self.refresh_thread = CachedBackendClient.RefreshThread(self, self.update_interval_ms)
        self.refresh_thread.start()

    def get_contents(self) -> Optional[GetRepositoryContentsResponse]:
        if not self._client:
            return None
        return self._client.GetRepositoryContents(
            GetRepositoryContentsRequest(repo_key=self.repository, session_key=self.session_key)
        )

    def update_store(self):
        self.load()

    def should_update_store(self):
        if not self._client:
            return
        version_response = self._client.GetRepositoryVersion(
            GetRepositoryVersionRequest(repo_key=self.repository, session_key=self.session_key)
        )
        current_sha = self.store.commit_sha
        return current_sha != version_response.commit_sha

    def close(self):
        super().close()
        self.refresh_thread.stop()
