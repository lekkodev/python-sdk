"""Lekko Python SDK Client"""

__version__ = "0.1"

LEKKO_API_URL = "prod.api.lekko.dev:443"
LEKKO_SIDECAR_URL = "localhost:50051"

from lekko_client.client import APIClient, SidecarClient  # noqa
from lekko_client.exceptions import *  # noqa
