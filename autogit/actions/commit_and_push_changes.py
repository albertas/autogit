import git

from autogit.constants import ModificationState
from autogit.data_types import RepoState
from autogit.utils.throttled_tasks_executor import ThrottledTasksExecutor


async def commit_and_push_changes(repo: RepoState) -> None:
    g = git.Repo(repo.directory)

    if g.index.diff(None) or g.untracked_files:
        g.git.add(A=True)
        g.git.commit(m=repo.args.commit_message)

        g.git.push('--set-upstream', 'origin', repo.branch)
        repo.modification_state = ModificationState.PUSHED_TO_REMOTE.value
    else:
        repo.modification_state = ModificationState.NO_FILES_CHANGED.value


def print_modified_repositories(repos: dict[str, RepoState]):
    print()
    branch = next(iter(repos.values())).branch
    print('\033[1;34m|' + f'Created branch: {branch}'.center(77, '-') + '|\033[0m')
    should_print_not_modified_repos = False
    print_repo_exceptions = False
    for repo in repos.values():
        if repo.modification_state == ModificationState.PUSHED_TO_REMOTE.value:
            print(f'\033[1;34m|\033[0m - {repo.url.ljust(73, " ")} \033[1;34m|\033[0m')
        else:
            if repo.modification_state == ModificationState.GOT_EXCEPTION.value:
                print_repo_exceptions = True
            should_print_not_modified_repos = True

    if should_print_not_modified_repos:
        print(
            '\033[1;34m|\033[0m'
            + 'Did NOT modify these repositories:'.center(77, '-')
            + '\033[1;34m|\033[0m'
        )
        for repo in repos.values():
            if repo.cloning_state != ModificationState.PUSHED_TO_REMOTE.value:
                print(
                    f'\033[1;34m|\033[0m - {(repo.url + " " + repo.modification_state).ljust(73, " ")} \033[1;34m|\033[0m'
                )

    if print_repo_exceptions:
        print(
            '\033[1;34m|\033[0m' + 'Exceptions:'.center(77, '-') + '\033[1;34m|\033[0m'
        )
        for repo in repos.values():
            if repo.cloning_state == ModificationState.GOT_EXCEPTION.value:
                print(
                    '\033[1;34m|\033[0m'
                     f' - {(repo.url + " " + repo.modification_state).ljust(73, " ")}:'
                     '\033[1;34m|\033[0m'
                )
                print(repo.stderr)

    print('\033[1;34m|' + ''.center(77, '-') + '|\033[0m')


def commit_and_push_changes_for_each_repo(
    repos: dict[str, RepoState], executor: ThrottledTasksExecutor
) -> None:
    for repo in repos.values():
        executor.run(commit_and_push_changes(repo))
    executor.wait_for_tasks_to_finish()
    print_modified_repositories(repos)
