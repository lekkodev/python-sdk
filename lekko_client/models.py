from dataclasses import dataclass
from typing import Dict, Optional

from lekko_client.gen.lekko.client.v1beta1.configuration_service_pb2 import Value
from lekko_client.gen.lekko.feature.v1beta1.feature_pb2 import Feature

ClientContext = Optional[Dict[str, Value]]


@dataclass
class ConfigData:
    config_sha: str
    config: Feature
