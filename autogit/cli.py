import asyncio
import sys


from autogit.actions._1_parse_arguments import parse_command_line_arguments
from autogit.actions._2_get_repository_states import get_repository_states
from autogit.actions._3_process_repo_to_create_pull_request import start_repos_processing_to_create_pull_requests
from autogit.actions._4_show import (
    show_repos_pull_request_creation_states_until_tasks_are_completed,
    show_pull_requests,
    show_exception_file_paths,
)

from autogit.utils.throttled_tasks_executor import ThrottledTasksExecutor


async def async_main(args: list[str] | None = None) -> None:
    cli_args = parse_command_line_arguments(args)
    repos = get_repository_states(cli_args)

    async with ThrottledTasksExecutor(delay_between_tasks=0.1) as executor:
        await start_repos_processing_to_create_pull_requests(repos, executor)
        await show_repos_pull_request_creation_states_until_tasks_are_completed(repos, executor)

    show_pull_requests(repos)
    show_exception_file_paths(repos)


def main(args: list[str] | None = None):
    asyncio.run(async_main(args))


if __name__ == '__main__':
    main()
