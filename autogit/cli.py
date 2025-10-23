import asyncio
import sys

from autogit.actions._1_parse_arguments import parse_command_line_arguments
from autogit.actions._2_get_repository_states import get_repository_states
from autogit.actions._4_clone_repositories import clone_repositories
from autogit.actions._5_create_branch import create_branch_for_each_repo
from autogit.actions._6_run_command import run_command_for_each_repo
from autogit.actions._7_commit_and_push_changes import (
    commit_and_push_changes_for_each_repo,
)
from autogit.actions._8_create_pull_request import create_pull_request_for_each_repo
from autogit.utils.print import print_failure
from autogit.utils.throttled_tasks_executor import ThrottledTasksExecutor


async def async_main(args: list[str] | None = None) -> None:
    cli_args = parse_command_line_arguments(args)
    repos = get_repository_states(cli_args)

    async with ThrottledTasksExecutor(delay_between_tasks=0.1) as executor:
        if not await clone_repositories(repos, executor):
            print_failure('Failed to clone some of the repositories.')
            sys.exit()
        await create_branch_for_each_repo(repos, executor)
        await run_command_for_each_repo(repos, executor)
        await commit_and_push_changes_for_each_repo(repos, executor)
        await create_pull_request_for_each_repo(repos, executor)


def main(args: list[str] | None = None):
    asyncio.run(async_main(args))


if __name__ == '__main__':
    main()
