from unittest import mock

import lekko_client
import pytest
from lekko_client.clients.cached_git_client import CachedGitClient
from lekko_client.gen.lekko.backend.v1beta1.distribution_service_pb2 import (
    GetRepositoryContentsResponse,
)


# Test that initialization doesn't cause errors
def test_init():
    with mock.patch.object(CachedGitClient, "load_contents", lambda _: GetRepositoryContentsResponse()):
        try:
            lekko_client.initialize(
                lekko_client.CachedGitConfig(
                    owner_name="test_owner",
                    repo_name="test_repo",
                    git_repo_path="",
                )
            )
        except:
            pytest.fail("cached git client initialization failed")
