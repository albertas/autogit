import argparse
from argparse import Namespace
import sys
from typing import Dict, Optional, Sequence


def parse_cli_arguments(args: Optional[Sequence[str]] = None) -> Namespace:
    if args is None:
        args = sys.argv

    parser = argparse.ArgumentParser(
        description="Update multiple GitLab or GitHub repositories with a single command.",
        epilog="""Report bugs and request features at https://github.com/albertas/git-multi-repo-updater/issues""",
        add_help=False)

    group_update = parser.add_argument_group("updating repositories")

    group_update.add_argument(
        "-r", "--repos", action='append', dest="repos", nargs="+",
        type=str, help="Repository url or Path to a file containing list of repository urls")

    group_update.add_argument(
        "-h", "--help", action="help", default=argparse.SUPPRESS,
        help="Show this message and exit.")

    parsed_args = parser.parse_args(args=args)
    parsed_args.repos = [repo for repo_list in parsed_args.repos for repo in repo_list]

    return parsed_args


def main():
    args = parse_cli_arguments()


if __name__ == "__main__":
    main()
