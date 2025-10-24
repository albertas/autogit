import asyncio
import sys

from autogit.actions._1_parse_arguments import parse_command_line_arguments
from autogit.actions._2_get_repository_states import get_repository_states
from autogit.actions._41_clone_repositories import clone_repositories
from autogit.actions._4b_create_branch import create_branch_for_each_repo
from autogit.actions._4c_run_command import run_command_for_each_repo
from autogit.actions._4d_commit_and_push_changes import (
    commit_and_push_changes_for_each_repo,
)
from autogit.actions._4e_create_pull_request import create_pull_request_for_each_repo
from autogit.utils._5_show import show_failure
from autogit.utils.throttled_tasks_executor import ThrottledTasksExecutor

from autogit.actions._4_process_repo_to_create_pull_request import start_repos_processing_to_create_pull_requests
from autogit.actions._5_show import show_repos_pull_request_creation_states_until_tasks_are_completed


async def async_main(args: list[str] | None = None) -> None:
    cli_args = parse_command_line_arguments(args)
    repos = get_repository_states(cli_args)

    async with ThrottledTasksExecutor(delay_between_tasks=0.1) as executor:
        start_repos_processing_to_create_pull_requests(repos, executor)
        await show_repos_pull_request_creation_states_until_tasks_are_completed(repos, executor)


def main(args: list[str] | None = None):
    asyncio.run(async_main(args))


if __name__ == '__main__':
    main()
