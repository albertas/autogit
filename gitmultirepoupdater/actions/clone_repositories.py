import logging
import os.path

import git

from gitmultirepoupdater.data_types import RepoState
from gitmultirepoupdater.constants import CloningStates
from gitmultirepoupdater.utils.throttled_tasks_executor import ThrottledTasksExecutor

logger = logging.getLogger()


async def clone_repository(repo_state: RepoState) -> None:
    clone_to = repo_state.args.clone_to
    repo_path = os.path.join(clone_to, repo_state.repo_name)

    # TODO: add a way to clone using access token: https://stackoverflow.com/questions/25409700/using-gitlab-token-to-clone-without-authentication/29570677#29570677
    # git clone https://:YOURKEY@your.gilab.company.org/group/project.git

    # TODO: add ssh support: urls like git@gitlab.com:niekas/gitlab-api-tests.git


    try:
        if os.path.exists(repo_path):  # If repository exists: clean it, pull changes, checkout correct branch
            logger.warning("Repository already exists, cleaning it")
            g = git.cmd.Git(repo_path)
            g.clean("-dfx")

            # Update symbolic-refs: git remote set-head origin --auto
            #   get main branch name:
            #   git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'
            # Switch to main branch

        else:
            logger.warning(f"Cloning {repo_state.repo_url} to {clone_to}")

            git.Repo.clone_from(repo_state.repo_url, repo_path)
            repo_state.cloning_state = CloningStates.CLONED.value
            repo_state.repo_path = repo_path

            logger.warning(f"Cloned repo from {repo_state.repo_url} to {clone_to}")

    except git.exc.GitCommandError:
        repo_state.cloning_state = CloningStates.NOT_FOUND.value
        # TODO: logging level is incorrect (its set to warning).
        logger.warning("Failed to clone repository", exc_info=True)


def clone_repositories(repo_states: dict[str, RepoState], executor: ThrottledTasksExecutor) -> None:
    for repo_state in repo_states.values():
        executor.run(clone_repository(repo_state))
    executor.wait_for_tasks_to_finish()
