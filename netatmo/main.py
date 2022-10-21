from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from typing import Optional

from dotenv import load_dotenv
from typed_argparse import TypedArgs

from . import __version__
from .netatmo import get_oauth_token, get_station_data


class Args(TypedArgs):
    env_file: Optional[str]
    out: str
    indent: int


class ArgParseCustomFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


def check_isfile(v: str) -> str:
    if os.path.isfile(v):
        return v
    else:
        raise argparse.ArgumentTypeError(f"{repr(v)} is not file.")


def parse_args(args: list[str] = sys.argv[1:]) -> Args:
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        prog="netatmo",
        formatter_class=(
            lambda prog: ArgParseCustomFormatter(
                prog,
                **{
                    "width": shutil.get_terminal_size(fallback=(120, 50)).columns,
                    "max_help_position": 25,
                },
            )
        ),
        description="Get netatmo information",
    )
    parser.add_argument(
        "-e", "--env_file", metavar="FILE", type=check_isfile, help="key file"
    )
    parser.add_argument(
        "-o",
        "--out",
        metavar="FILE",
        type=str,
        help="log file name",
        default="log.json",
    )
    parser.add_argument(
        "-i",
        "--indent",
        metavar="INT",
        type=int,
        help="indentation of log.json",
        default=2,
    )
    parser.add_argument("-V", "--version", action="version", version=__version__)

    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)
    else:
        return Args.from_argparse(parser.parse_args())


def main() -> None:
    args = parse_args()
    load_dotenv(args.env_file)

    try:
        chilent_id = os.environ["CLIENT_ID"]
        client_secret = os.environ["CLIENT_SECRET"]
        username = os.environ["USERNAME"]
        password = os.environ["PASSWORD"]
    except KeyError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    oauth_token = get_oauth_token(chilent_id, client_secret, username, password)
    data = get_station_data(oauth_token)

    print(
        json.dumps(data, indent=args.indent, ensure_ascii=False),
        file=open(args.out, "w"),
    )


if __name__ == "__main__":
    main()
