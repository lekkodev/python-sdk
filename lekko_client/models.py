from dataclasses import dataclass

from lekko_client.gen.lekko.feature.v1beta1.feature_pb2 import Feature


@dataclass
class FeatureData:
    config_sha: str
    feature: Feature
