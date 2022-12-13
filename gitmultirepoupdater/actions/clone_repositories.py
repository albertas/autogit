import logging
import os.path

import git
from git.cmd import Git

from gitmultirepoupdater.data_types import RepoState
from gitmultirepoupdater.constants import CloningStates
from gitmultirepoupdater.utils.throttled_tasks_executor import ThrottledTasksExecutor

logger = logging.getLogger()


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

            git.Repo.clone_from(repo.url, repo_directory)
            repo.cloning_state = CloningStates.CLONED.value
            repo.directory = repo_directory

            logger.warning(f"Cloned repo from {repo.url} to {clone_to}")

        set_target_branch_if_not_set(repo)

    except git.exc.GitCommandError:
        repo.cloning_state = CloningStates.NOT_FOUND.value
        # TODO: logging level is incorrect (its set to warning).
        logger.warning("Failed to clone repository", exc_info=True)


def clone_repositories(repos: dict[str, RepoState], executor: ThrottledTasksExecutor) -> None:
    for repo in repos.values():
        executor.run(clone_repository(repo))
    executor.wait_for_tasks_to_finish()
