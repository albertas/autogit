import git
from logging import getLogger

from gitmultirepoupdater.data_types import RepoState
from gitmultirepoupdater.utils.throttled_tasks_executor import ThrottledTasksExecutor

logger = getLogger()


async def commit_and_push_changes(repo: RepoState) -> None:
    g = git.Repo(repo.directory)

    if g.index.diff(None) or g.untracked_files:
        g.git.add(A=True)
        g.git.commit(m=repo.args.commit_message)
        logger.warning("Created commit for newest changes")

        g.git.push("--set-upstream", "origin", repo.branch)
        logger.warning("Pushed changes to upstream")
    else:
        logger.warning("No changes were made")


def commit_and_push_changes_for_each_repo(repos: dict[str, RepoState], executor: ThrottledTasksExecutor) -> None:
    for repo in repos.values():
        executor.run(commit_and_push_changes(repo))
    executor.wait_for_tasks_to_finish()
