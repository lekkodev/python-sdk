import glob
import os
from typing import Any, Dict, List, Optional

import grpc
import yaml
from dulwich.errors import NotGitRepository
from dulwich.object_store import tree_lookup_path
from dulwich.repo import Repo as GitRepo
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver

from lekko_client.clients.distribution_client import CachedDistributionClient
from lekko_client.exceptions import GitRepoNotFound
from lekko_client.gen.lekko.backend.v1beta1.distribution_service_pb2 import (
    Feature as DistFeature,
)
from lekko_client.gen.lekko.backend.v1beta1.distribution_service_pb2 import (
    GetRepositoryContentsResponse,
    Namespace,
)
from lekko_client.gen.lekko.feature.v1beta1.feature_pb2 import Feature
from lekko_client.stores.store import Store


class CachedGitClient(CachedDistributionClient):
    ROOT_CONFIG_METADATA_FILENAME = "lekko.root.yaml"

    class GitFileEventHandler(FileSystemEventHandler):
        def __init__(self, client: "CachedGitClient") -> None:
            super().__init__()
            self.client = client

        def on_any_event(self, event):
            self.client.load()
            return super().on_any_event(event)

    def __init__(
        self,
        lekko_uri: str,
        repository_owner: str,
        repository_name: str,
        store: Store,
        path: str,
        api_key: Optional[str],
        context: Optional[Dict[str, Any]] = None,
        credentials: grpc.ChannelCredentials = grpc.ssl_channel_credentials(),
        should_watch: Optional[bool] = True,
    ):
        super().__init__(lekko_uri, repository_owner, repository_name, store, api_key, context, credentials)
        self.watcher: Optional[BaseObserver] = None
        self.path = path
        self.should_watch = should_watch

    def initialize(self) -> None:
        super().initialize()
        self.load()
        if self.should_watch:
            event_handler = CachedGitClient.GitFileEventHandler(self)
            self.watcher = Observer()
            self.watcher.schedule(event_handler, self.path, recursive=True)
            self.watcher.start()

    def load_contents(self) -> GetRepositoryContentsResponse:
        try:
            repo = GitRepo(self.path)
        except NotGitRepository:
            raise GitRepoNotFound(f"{self.path} is not a git repository")

        return GetRepositoryContentsResponse(
            commit_sha=repo.head().decode("utf-8"), namespaces=self.get_namespaces(repo)
        )

    def get_namespaces(self, repo: GitRepo) -> List[Namespace]:
        md_file_path = os.path.join(self.path, self.ROOT_CONFIG_METADATA_FILENAME)
        with open(md_file_path) as f:
            md_contents = yaml.safe_load(f)

        ns_names = md_contents.get("namespaces", [])
        return [Namespace(name=ns_name, features=self.get_configs(repo, ns_name)) for ns_name in ns_names]

    def get_configs(self, repo: GitRepo, ns_name: str) -> List[DistFeature]:
        proto_dir_path = os.path.join(self.path, ns_name, "gen", "proto")
        if not os.path.isdir(proto_dir_path):
            return []

        features = []
        for proto_bin_file in glob.glob(os.path.join(proto_dir_path, "*.proto.bin")):
            proto_bin_relative_filename = os.path.relpath(proto_bin_file, self.path)
            with open(proto_bin_file, "rb") as proto_bin:
                _, sha = tree_lookup_path(
                    repo.get_object, repo[repo.head()].tree, proto_bin_relative_filename.encode()  # type: ignore
                )
                feature = Feature()
                feature.ParseFromString(proto_bin.read())
                features.append(
                    DistFeature(
                        name=os.path.basename(proto_bin_file).replace(".proto.bin", ""),
                        sha=sha.decode("utf-8"),
                        feature=feature,
                    )
                )
        return features

    def close(self):
        super().close()
        # if self.events_batcher:
        # await self.events_batcher.close()
        if self.watcher:
            self.watcher.stop()
            self.watcher.join()
