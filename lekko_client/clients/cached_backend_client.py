import logging
import time
from threading import Event, Thread
from typing import Any, Dict, Optional

import grpc
from google.protobuf.any_pb2 import Any as ProtoAny

from lekko_client.clients.distribution_client import CachedDistributionClient
from lekko_client.exceptions import ClientNotInitialized
from lekko_client.gen.lekko.backend.v1beta1.distribution_service_pb2 import (
    GetRepositoryContentsRequest,
    GetRepositoryContentsResponse,
    GetRepositoryVersionRequest,
)
from lekko_client.stores.store import Store

log = logging.getLogger(__name__)


class CachedBackendClient(CachedDistributionClient):
    class RefreshThread(Thread):
        def __init__(self, client: "CachedBackendClient", refresh_interval_ms: int):
            super().__init__()
            self.daemon = True
            self.client = client
            self.refresh_interval = refresh_interval_ms
            self._enabled = True

        def stop(self) -> None:
            self._enabled = False

        def run(self) -> None:
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
        *,
        update_interval_ms: int,
    ) -> None:
        self.update_interval_ms = update_interval_ms
        self.timeout = None
        self.closed = False
        self.initialized_event = Event()
        super().__init__(uri, owner_name, repo_name, store, api_key, context, credentials)

    def initialize(self) -> None:
        super().initialize()
        self.refresh_thread = CachedBackendClient.RefreshThread(self, self.update_interval_ms)
        self.refresh_thread.start()

    def load_contents(self) -> Optional[GetRepositoryContentsResponse]:
        if not self._client:
            return None
        return self._client.GetRepositoryContents(
            GetRepositoryContentsRequest(repo_key=self.repository, session_key=self.session_key)
        )

    def update_store(self) -> None:
        self.load()
        self.initialized_event.set()

    def should_update_store(self) -> bool:
        if not self._client:
            return False
        if not self.initialized_event.is_set():
            return True
        try:
            version_response = self._client.GetRepositoryVersion(
                GetRepositoryVersionRequest(repo_key=self.repository, session_key=self.session_key)
            )
        except Exception:
            log.warning("Failed to fetch latest repository version", exc_info=True)
            return False
        current_sha = self.store.commit_sha
        return current_sha != version_response.commit_sha

    def close(self) -> None:
        super().close()
        self.refresh_thread.stop()
        self.initialized_event.clear()

    def get(self, namespace: str, key: str, context: Dict[str, Any]) -> ProtoAny:
        if not self.initialized_event.wait(timeout=5):  # Give the background thread 5 seconds to populate
            raise ClientNotInitialized("Repository contents not yet loaded from server")
        return super().get(namespace, key, context)
