import git
from logging import getLogger

from gitmultirepoupdater.data_types import RepoState
from gitmultirepoupdater.utils.throttled_tasks_executor import ThrottledTasksExecutor

logger = getLogger()


async def commit_and_push_changes(repo_state: RepoState) -> None:
    repo = git.Repo(repo_state.repo_path) 

    if repo.index.diff(None) or repo.untracked_files:
        repo.git.add(A=True)
        repo.git.commit(m=repo_state.args.commit_message)
        logger.warning("Created commit for newest changes")

        repo.git.push("--set-upstream", "origin", repo_state.branch_name)
        logger.warning("Pushed changes to upstream")
    else:
        logger.warning("No changes were made")


def commit_and_push_changes_for_each_repo(repo_states: dict[str, RepoState], executor: ThrottledTasksExecutor) -> None:
    for repo_state in repo_states.values():
        executor.run(commit_and_push_changes(repo_state))
    executor.wait_for_tasks_to_finish()
