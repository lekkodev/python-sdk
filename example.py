import argparse

import grpc
from google.protobuf.json_format import MessageToDict

from lekko_client import APIClient, SidecarClient
from lekko_client.exceptions import LekkoError

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apikey", type=str)
    parser.add_argument("--sidecar", action="store_true")
    parser.add_argument("--owner", type=str)
    parser.add_argument("--repo", type=str)
    parser.add_argument("--namespace", type=str)
    parser.add_argument("--feature", type=str)
    parser.add_argument(
        "--feature-type",
        type=str,
        choices=["bool", "int", "float", "str", "json", "proto"],
        default="str",
    )
    parser.add_argument("--proto-type", type=str, default="")
    parser.add_argument("--proto-file", type=str)
    args = parser.parse_args()

    client_cls = SidecarClient if args.sidecar else APIClient
    client = client_cls(args.owner, args.repo, args.namespace, api_key=args.apikey)

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
            if not args.proto_file:
                print(
                    "Must provide a --proto-file. Could be a path or a well-known proto like 'google/protobuf/wrappers.proto'"
                )
            else:
                imported_proto = grpc.protos(args.proto_file)

                if args.proto_type:
                    msg_type = getattr(imported_proto, args.proto_type)
                    val = MessageToDict(client.get_proto_by_type(args.feature, {}, msg_type))
                else:
                    val = MessageToDict(client.get_proto(args.feature, {}))
        print(f"Got {val} for feature")
    except LekkoError as e:
        print(f"Failed to get feature: {e}")
        if e.__cause__:
            print(f"Caused by: {e.__cause__}")
