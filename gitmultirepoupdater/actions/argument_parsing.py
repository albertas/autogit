import argparse
import logging
import sys
from argparse import Namespace
from typing import Optional

from gitmultirepoupdater.utils.helpers import flatten_list, get_random_hex


def get_argument_parser():
    parser = argparse.ArgumentParser(
        description="Update multiple GitLab or GitHub repositories with a single command.",
        epilog="""Report bugs and request features at https://github.com/albertas/git-multi-repo-updater/issues""",
        add_help=False)

    parser.add_argument(
        "-r", "--repos", action="append", dest="repos", nargs="?", default=[],
        type=str, help="Repository url or Path to a file containing list of repository urls")

    parser.add_argument(
        "-c", "--clone-to", action="store", dest="clone_to", default="/tmp/", type=str, nargs="?",
        help="Path to directory which will be used to clone git repositories to (default is /tmp/)")

    parser.add_argument(
        "-m", "--message", "--commit-message", action="store", dest="commit_message",
        default=f"Git multi repo updater action #{get_random_hex()}", type=str, nargs="?",
        help="Message which will be used for commit message (and for branch name, PR title if they are not specified)")

    parser.add_argument(
        "-v", "--verbose", action=argparse.BooleanOptionalAction, dest="verbose",
        default=False, type=bool,
        help="Increase verbosity and show DEBUG logs")

    parser.add_argument(
        "-h", "--help", action="help", default=argparse.SUPPRESS,
        help="Show this message and exit.")

    parser.add_argument(
        "commands", type=str, nargs="*",
        help="Commands or scripts to execute in local Git repository")

    return parser


def parse_command_line_arguments(args: Optional[list[str]] = None) -> Namespace:
    if args is None:
        args = sys.argv[1:]

    parser = get_argument_parser()
    parsed_args = parser.parse_args(args=args)

    if parsed_args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # parsed_args.repos = flatten_list(parsed_args.repos)

    return parsed_args
