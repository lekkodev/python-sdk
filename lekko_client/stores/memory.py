from typing import Dict

from lekko_client.models import FeatureData
from lekko_client.stores.store import Store


class MemoryStore(Store):
    def __init__(self):
        super().__init__()
        self.configs: Dict[str, Dict[str, FeatureData]] = {}

    def get(self, namespace: str, config_key: str) -> FeatureData:
        namespace_map = self.configs.get(namespace)
        if not namespace_map:
            raise Exception("namespace not found")
        result = namespace_map.get(config_key)
        if not result:
            raise Exception("config not found")
        return result

    def load_impl(self, contents) -> bool:
        new_configs = {}
        for ns in contents.namespaces:
            namespace_map = {}
            for cfg in ns.features:
                if cfg.feature:
                    namespace_map[cfg.name] = FeatureData(cfg.sha, cfg.feature)
            new_configs[ns.name] = namespace_map
        self.configs = new_configs
        return True
