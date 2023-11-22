from unittest import mock

import lekko_client


def test_init():
    with mock.patch("lekko_client.clients.distribution_client.DistributionServiceStub") as stub:
        stub().RegisterClient.return_value = mock.Mock(session_key="test_session_key")
        lekko_client.initialize(
            lekko_client.CachedServerConfig(
                owner_name="test_owner",
                repo_name="test_repo",
                api_key="test_api_key",
            )
        )
