import argparse
import dataclasses

import grpc
from google.protobuf.json_format import MessageToDict

import lekko_client
from lekko_client.exceptions import LekkoError

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apikey", type=str)
    parser.add_argument("--mode", type=str, choices=["sidecar", "api", "cachedapi", "cachedgit"])
    parser.add_argument("--owner", type=str)
    parser.add_argument("--repo", type=str)
    parser.add_argument("--namespace", type=str, default="default")
    parser.add_argument("--config", type=str, default="example")
    parser.add_argument(
        "--config-type",
        type=str,
        choices=["bool", "int", "float", "str", "json", "proto"],
        default="bool",
    )
    parser.add_argument("--git-path", type=str, default="")
    parser.add_argument("--proto-type", type=str, default="")
    parser.add_argument("--proto-file", type=str)
    args = parser.parse_args()

    # client_cls = SidecarClient if args.sidecar else APIClient

    base_config = lekko_client.Config(owner_name=args.owner, repo_name=args.repo, api_key=args.apikey)
    if args.mode == "sidecar":
        config = lekko_client.SidecarConfig(**dataclasses.asdict(base_config))
    elif args.mode == "api":
        config = lekko_client.APIConfig(**dataclasses.asdict(base_config))
    elif args.mode == "cachedapi":
        config = lekko_client.CachedServerConfig(**dataclasses.asdict(base_config))
    elif args.mode == "cachedgit":
        config = lekko_client.CachedGitConfig(**dataclasses.asdict(base_config), git_repo_path=args.git_path)
    else:
        raise ValueError("Invalid mode")
    lekko_client.initialize(config)

    val = None
    try:
        if args.config_type == "bool":
            val = lekko_client.get_bool(args.namespace, args.config, {})
        elif args.config_type == "int":
            val = lekko_client.get_int(args.namespace, args.config, {})
        elif args.config_type == "str":
            val = lekko_client.get_string(args.namespace, args.config, {})
        elif args.config_type == "json":
            val = lekko_client.get_json(args.namespace, args.config, {})
        elif args.config_type == "float":
            val = lekko_client.get_float(args.namespace, args.config, {})
        elif args.config_type == "proto":
            if not args.proto_file:
                print(
                    "Must provide a --proto-file. Could be a path or a well-known proto like 'google/protobuf/wrappers.proto'"
                )
            else:
                imported_proto = grpc.protos(args.proto_file)

                if args.proto_type:
                    msg_type = getattr(imported_proto, args.proto_type)
                    val = MessageToDict(lekko_client.get_proto_by_type(args.namespace, args.config, {}, msg_type))
                else:
                    val = MessageToDict(lekko_client.get_proto(args.namespace, args.config, {}))
        print(f"Got {val} for config {args.namespace}/{args.config}")
    except LekkoError as e:
        print(f"Failed to get config: {e}")
        if e.__cause__:
            print(f"Caused by: {e.__cause__}")
