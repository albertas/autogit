"""
Display PR creation progress interactively in the terminal.
Show repository link and PR creation state that is being executed right now.

Key features of this file are:
 - single repo PR creation state display function for a single line.
 - group repo PR creation state display rerendered based on repos state.
 - display repo PR creation states until all executor tasks are finished.
"""

def get_repo_state_line(repo: RepoState):
    state_line = f'{repo.url}  '

    # TODO: Have states for each of these steps:
    # await clone_repository(repo)
    # await create_branch(repo)
    # await run_command(repo)
    # await commit_and_push_changes(repo)
    # await create_pull_request(repo)

    # TODO: Flashing text protection: show percent of the processing. Only show error codes.

    # TODO: Branch name will not be printed. Should ensure it will be printed in a separate line.

    # TODO: Percent % and gray text was being done for that repository right now.
    # Error should be shown in Yellow/White.

    if pull_request_state_label := repo.pull_request_state_label:
        state_line += pull_request_state_label
    elif modification_state_label := repo.modification_state_label:
        state_line += modification_state_label
    elif cloning_state_label := repo.cloning_state_label:
        state_line += cloning_state_label

    return state_line


def get_repos_state_lines(repos: dict[str, RepoState]):
    lines = [Text(get_repo_state_line(repo)) for repo in repos.values()]
    return Group(*lines)


async def show_repos_pull_request_creation_states_until_tasks_are_completed(
    repos: dict[str, RepoState], executor: ThrottledTasksExecutor
):
    """Interactively show repository PR creation state by updating
    shown CLI information for each repository.
    """
    console = Console()
    with Live(get_repos_state_lines(repos), console=console, refresh_per_second=5) as live:
        while executor.running_tasks:
            live.update(get_repos_state_lines(repos))
            await asyncio.sleep(0.1)
        live.update(get_repos_state_lines(repos))


def show_pull_requests(repos):
    print('\n\033[1;32m' + 'Created Pull Requests'.center(79, ' ') + '\033[0m')
    for repo in repos.values():
        if repo.pull_request_state == PullRequestStates.CREATED.value:
            print(f'\033[1;32m\033[0m {repo.pull_request_url.ljust(77, " ")} \033[1;32m\033[0m')


def show_failure(message: str) -> None:
    return print('\n\033[1;31m' + message.center(79, ' ') + '\033[0m')
