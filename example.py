import argparse

from google.protobuf import wrappers_pb2 as wrappers
from google.protobuf.any_pb2 import Any as AnyProto

from lekko_client import LEKKO_API_URL, LEKKO_SIDECAR_URL, Client
from lekko_client.exceptions import LekkoError


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apikey", type=str)
    parser.add_argument("--sidecar", action="store_true")
    parser.add_argument("--owner", type=str)
    parser.add_argument("--repo", type=str)
    parser.add_argument("--namespace", type=str)
    parser.add_argument("--feature", type=str)
    parser.add_argument("--feature-type", type=str, choices=["bool", "int", "float", "str", "json", "proto"], default="str")
    parser.add_argument("--proto-type", type=str, default="")
    args = parser.parse_args()

    uri = LEKKO_SIDECAR_URL if args.sidecar else LEKKO_API_URL
    client = Client(uri, args.owner, args.repo, args.namespace, api_key=args.apikey)

    val = None
    try:
        if args.feature_type == "bool":
            val = client.get_bool(args.feature, {})
        elif args.feature_type == "int":
            val = client.get_int(args.feature, {})
        elif args.feature_type == "str":
            val = client.get_string(args.feature, {})
        elif args.feature_type == "json":
            val = client.get_json(args.feature, {})
        elif args.feature_type == "float":
            val = client.get_float(args.feature, {})
        elif args.feature_type == "proto":
            msg_type = getattr(wrappers, args.proto_type, AnyProto)
            val = client.get_proto(args.feature, {}, msg_type)
        print(f"Got {val} for feature")
    except LekkoError as e:
        print(f"Failed to get feature: {e}")
        if e.__cause__:
            print(f"Caused by: {e.__cause__}")
