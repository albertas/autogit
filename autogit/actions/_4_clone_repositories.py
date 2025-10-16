import sys
import os
from pathlib import Path
from urllib.parse import urlparse

import git
from git.cmd import Git
from git.exc import GitCommandError

from autogit.constants import CloningStates
from autogit.data_types import RepoState
from autogit.utils.helpers import get_access_token, get_default_branch
from autogit.utils.print import print_failure
from autogit.utils.throttled_tasks_executor import ThrottledTasksExecutor


def get_repo_access_url(url: str) -> str | None:
    """Converts repository url to url which is suitable for cloning."""
    if url.startswith('http'):
        if access_token := get_access_token(url):
            parsed_url = urlparse(url)
            domain_with_access_token = f'api:{access_token}@{parsed_url.netloc.split("@")[-1]}'
            parsed_url = parsed_url._replace(netloc=domain_with_access_token, scheme='https')
            return parsed_url.geturl()
    elif url.startswith('git@'):
        return url
    return None


async def clone_repository(repo: RepoState) -> None:
    """Clones repository with default (or source) branch."""
    clone_to = repo.args.clone_to
    repo.directory = str((Path(clone_to) / repo.name).expanduser())

    # TODO: add a way to clone using access token: https://stackoverflow.com/questions/25409700/using-gitlab-token-to-clone-without-authentication/29570677#29570677
    # git clone https://:YOURKEY@your.gilab.company.org/group/project.git

    # TODO: add ssh support: urls like git@gitlab.com:niekas/gitlab-api-tests.git

    try:
        directory = Path(repo.directory)
        if directory.exists():
            ## TODO: check if directory exist
            # if directory.iterdir() and not (Path(repo.directory) / '.git/').exists():
            #     print_failure(f'This is not a Git directory (wanted to clone to it): {repo.directory}')
            #     repo.cloning_state = CloningStates.DIRECTORY_NOT_EMPTY.value
            #     return

            # If repository exists: clean it, pull changes, checkout default branch
            g: Git = Git(repo.directory)
            g.clean('-dfx')
            g.execute(['git', 'fetch', '--all'])

            repo.target_branch = repo.target_branch or get_default_branch(repo)
            repo.source_branch = repo.source_branch or repo.target_branch

            g.checkout(repo.source_branch)

            repo.cloning_state = CloningStates.CLONED.value
        elif repo_access_url := get_repo_access_url(repo.url):
            Path(repo.directory).mkdir(parents=True)
            git.Repo.clone_from(url=repo_access_url, to_path=repo.directory)

            g = Git(repo.directory)
            g.execute(['git', 'fetch', '--all'])

            repo.target_branch = repo.target_branch or get_default_branch(repo)
            repo.source_branch = repo.source_branch or repo.target_branch

            try:
                g.checkout(repo.source_branch)
            except git.exc.GitCommandError:
                repo.cloning_state = CloningStates.SOURCE_BRANCH_DOES_NOT_EXIST.value
            else:
                repo.cloning_state = CloningStates.CLONED.value
        else:
            repo.cloning_state = CloningStates.ACCESS_TOKEN_NOT_PROVIDED.value

    except GitCommandError:
        repo.cloning_state = CloningStates.NOT_FOUND.value


def print_cloned_repositories(repos):
    # TODO: flush print message after each repository action is done (not to freeze the screen if cloning multiple repositories takes too long)
    clone_to = next(iter(repos.values())).args.clone_to
    print('\n\033[1;32m' + f'Cloned repositories (to {clone_to})'.center(79, ' ') + '\033[0m')
    should_print_not_cloned_repos = False
    for repo in repos.values():
        if repo.cloning_state == CloningStates.CLONED.value:
            print(f'\033[1;32m\033[0m {repo.url.ljust(77, " ")} \033[1;32m\033[0m')
        else:
            should_print_not_cloned_repos = True
    if should_print_not_cloned_repos:
        print('\033[1;33m' + 'Did NOT clone these repositories:'.center(79, ' ') + '\033[0m')
        for repo in repos.values():
            if repo.cloning_state != CloningStates.CLONED.value:
                print(
                    f'{(repo.url + " \033[1;33m" + repo.cloning_state).ljust(77, " ")} \033[0m'
                )

def were_all_repositories_clonned_successfully(repos: dict[str, RepoState]) -> bool:
    return all(repo.cloning_state == CloningStates.CLONED.value for repo in repos.values())


def clone_repositories(repos: dict[str, RepoState], executor: ThrottledTasksExecutor) -> bool:
    """:return: were all repositories clonned successfully."""
    for repo in repos.values():
        executor.run(clone_repository(repo))
    executor.wait_for_tasks_to_finish()
    print_cloned_repositories(repos)
    return were_all_repositories_clonned_successfully(repos)
