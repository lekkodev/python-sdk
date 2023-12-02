from unittest import mock

import lekko_client
from lekko_client.gen.lekko.backend.v1beta1.distribution_service_pb2 import (
    GetRepositoryContentsResponse,
    GetRepositoryVersionResponse,
)


def test_init():
    with mock.patch("lekko_client.clients.distribution_client.DistributionServiceStub") as stub:
        stub().RegisterClient.return_value = mock.Mock(session_key="test_session_key")
        stub().GetRepositoryVersion.side_effect = [
            GetRepositoryVersionResponse(commit_sha="test_commit_sha1"),
            GetRepositoryVersionResponse(commit_sha="test_commit_sha2"),
        ]
        stub().GetRepositoryContents.return_value = GetRepositoryContentsResponse(
            commit_sha="test_commit_sha1", namespaces=[]
        )
        client = lekko_client.initialize(
            lekko_client.CachedServerConfig(
                owner_name="test_owner",
                repo_name="test_repo",
                api_key="test_api_key",
                update_interval_ms=0,
            )
        )
        assert client.initialized_event.wait(timeout=0.1)
        client.close()


def test_should_update_store():
    with mock.patch("lekko_client.clients.cached_backend_client.Event") as mock_event, mock.patch(
        "lekko_client.clients.distribution_client.DistributionServiceStub"
    ) as mock_stub:
        mock_event().is_set.return_value = True
        mock_stub().RegisterClient.return_value = mock.Mock(session_key="test_session_key")
        mock_stub().GetRepositoryVersion.side_effect = Exception("test")

        client = lekko_client.CachedBackendClient(
            uri="test_uri",
            store=lekko_client.MemoryStore(),
            owner_name="test_owner",
            repo_name="test_repo",
            api_key="test_api_key",
            update_interval_ms=0,
        )
        assert client.should_update_store() is False
