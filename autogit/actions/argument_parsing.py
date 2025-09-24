import argparse
import logging
import sys

from autogit.data_types import CliArguments
from autogit.utils.helpers import get_random_hex


def get_argument_parser() -> argparse.ArgumentParser:
    action_id = get_random_hex()

    parser = argparse.ArgumentParser(
        description='Update multiple GitLab or GitHub repositories with a single command.',
        epilog="""Report bugs and request features at https://github.com/albertas/auto-git/issues""",
        add_help=False,
    )

    parser.add_argument(
        '-r',
        '--repos',
        action='append',
        dest='repos',
        nargs='?',
        default=[],
        type=str,
        help='Repository url or Path to a file containing list of repository urls',
    )

    parser.add_argument(
        '-c',
        '--clone-to',
        action='store',
        dest='clone_to',
        default='/tmp/',
        type=str,
        nargs='?',
        help='Path to directory which will be used to clone git repositories to (default is /tmp/)',
    )

    parser.add_argument(
        '-m',
        '--message',
        '--commit-message',
        action='store',
        dest='commit_message',
        default=f'Auto Git action #{action_id}',
        type=str,
        nargs='?',
        help='Message which will be used for commit message (and for branch name, PR title if they are not specified)',
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_const',
        dest='verbose',
        default=False,
        const=True,
        help='Increase verbosity and show DEBUG logs',
    )

    parser.add_argument(
        '-b',
        '--branch',
        action='store',
        dest='branch',
        type=str,
        nargs='?',
        help='Branch name which will be used to apply changes (it will be created if it does not exist)',
    )

    parser.add_argument(
        '-t',
        '--target-branch',
        action='store',
        dest='target_branch',
        type=str,
        nargs='?',
        help='Target branch name which will be used to pull changes into',
    )

    parser.add_argument(
        '-h',
        '--help',
        action='help',
        default=argparse.SUPPRESS,
        help='Show this message and exit.',
    )

    parser.add_argument(
        'commands',
        type=str,
        nargs='*',
        help='Commands or scripts to execute in local Git repository',
    )

    parser.add_argument(
        '--action-id',
        action='store_const',
        dest='action_id',
        const=action_id,
        help='Unique hex for action identification',
    )

    return parser


def parse_command_line_arguments(args: list[str] | None = None) -> CliArguments:
    if args is None:
        args = sys.argv[1:]

    parser = get_argument_parser()
    parsed_args: CliArguments = parser.parse_args(args=args)  # type: ignore

    if parsed_args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    return parsed_args
