import logging
import os.path
from urllib.parse import urlparse

import git
from git.cmd import Git

from gitmultirepoupdater.data_types import RepoState
from gitmultirepoupdater.constants import CloningStates
from gitmultirepoupdater.utils.throttled_tasks_executor import ThrottledTasksExecutor
from gitmultirepoupdater.utils.helpers import get_access_token

logger = logging.getLogger()


def get_repo_access_url(url: str) -> str:
    """Converts repository url to url which is suitable for cloning"""

    if access_token := get_access_token(url):
        parsed_url = urlparse(url)
        domain_with_access_token = f"api:{access_token}@{parsed_url.netloc.split('@')[-1]}"
        parsed_url = parsed_url._replace(netloc=domain_with_access_token, scheme="https")
        return parsed_url.geturl()
    return url


def set_target_branch_if_not_set(repo: RepoState) -> None:
    if repo.target_branch:
        return

    g = Git(repo.directory)
    target_branch_name: str = g.execute(["git", "rev-parse", "--abbrev-ref", "origin/HEAD"])  # type: ignore
    target_branch_name = target_branch_name.split("/", 1)[-1]  # removes `origin/` prefix from the result
    repo.target_branch = target_branch_name
    return


async def clone_repository(repo: RepoState) -> None:
    clone_to = repo.args.clone_to
    repo_directory = os.path.join(clone_to, repo.name)

    # TODO: add a way to clone using access token: https://stackoverflow.com/questions/25409700/using-gitlab-token-to-clone-without-authentication/29570677#29570677
    # git clone https://:YOURKEY@your.gilab.company.org/group/project.git

    # TODO: add ssh support: urls like git@gitlab.com:niekas/gitlab-api-tests.git

    try:
        if os.path.exists(repo_directory):  # If repository exists: clean it, pull changes, checkout correct branch
            logger.warning("Repository already exists, cleaning it")
            g = Git(repo_directory)
            g.clean("-dfx")

            # TODO:
            # Update symbolic-refs: git remote set-head origin --auto
            #   get main branch name:
            #   git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'
            # Switch to main branch

        else:
            logger.warning(f"Cloning {repo.url} to {clone_to}")

            repo_access_url = get_repo_access_url(repo.url)
            git.Repo.clone_from(repo_access_url, repo_directory)
            repo.cloning_state = CloningStates.CLONED.value
            repo.directory = repo_directory

            logger.warning(f"Cloned repo from {repo.url} to {clone_to}")

        set_target_branch_if_not_set(repo)

    except git.exc.GitCommandError:
        repo.cloning_state = CloningStates.NOT_FOUND.value
        # TODO: logging level is incorrect (its set to warning).
        logger.warning("Failed to clone repository", exc_info=True)


def print_cloned_repositories(repos):
    print()
    print("\033[1;34m|" + "Cloned repositories".center(77, "-") + "|\033[0m")
    should_print_not_cloned_repos = False
    for repo in repos.values():
        if repo.cloning_state == CloningStates.CLONED.value:
            print(f"\033[1;34m|\033[0m - {repo.url.ljust(73, ' ')} \033[1;34m|\033[0m")
        else:
            should_print_not_cloned_repos = True
    if should_print_not_cloned_repos:
        print("\033[1;34m|\033[0m" + "Did NOT clone these repositories:".center(77, "-") + "\033[1;34m|\033[0m")
        for repo in repos.values():
            if repo.cloning_state != repo.cloning_state:
                print(f"\033[1;34m|\033[0m - {(repo.url + ' ' + CloningStates.CLONED.value).ljust(73, ' ')} \033[1;34m|\033[0m")
    print("\033[1;34m|" + "".center(77, "-") + "|\033[0m")


def clone_repositories(repos: dict[str, RepoState], executor: ThrottledTasksExecutor) -> None:
    for repo in repos.values():
        executor.run(clone_repository(repo))
    executor.wait_for_tasks_to_finish()
    print_cloned_repositories(repos)
