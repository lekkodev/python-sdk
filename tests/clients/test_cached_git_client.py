from unittest import mock

import pytest
from watchdog.observers import Observer

import lekko_client
from lekko_client.clients.cached_git_client import CachedGitClient
from lekko_client.gen.lekko.backend.v1beta1.distribution_service_pb2 import (
    GetRepositoryContentsResponse,
)


# Test that initialization doesn't cause errors
def test_init():
    with mock.patch.object(CachedGitClient, "load_contents", lambda _: GetRepositoryContentsResponse()):
        with mock.patch("watchdog.observers.Observer", spec_set=Observer):
            try:
                lekko_client.initialize(
                    lekko_client.CachedGitConfig(
                        owner_name="test_owner",
                        repo_name="test_repo",
                        git_repo_path="_test_/_path_",
                    )
                )
            except Exception:
                pytest.fail("cached git client initialization failed")
