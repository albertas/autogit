"""Provide async function for processing a single repository
to create Pull Request.

The processing of a repository consists of these steps:
- Clone repository
- Create branch
- Run command
- Commit changes
- Push changes to the remote repository
- Create Pull Request.
"""

from autogit.actions._3a_clone_repositories import clone_repository
from autogit.actions._3b_create_branch import create_branch
from autogit.actions._3c_run_command import run_command
from autogit.actions._3d_commit_and_push_changes import commit_and_push_changes
from autogit.actions._3e_create_pull_request import create_pull_request
from autogit.data_types import RepoState
from autogit.utils.throttled_tasks_executor import ThrottledTasksExecutor


async def process_repo(repo: RepoState) -> None:
    """Do all the steps needed to create a Pull Request."""
    if not await clone_repository(repo):
        return
    if not await create_branch(repo):
        return
    if not await run_command(repo):
        return
    if not await commit_and_push_changes(repo):
        return
    if not await create_pull_request(repo):
        return


async def start_repos_processing_to_create_pull_requests(
    repos: dict[str, RepoState], executor: ThrottledTasksExecutor
) -> None:
    """Submit repositories to be processed in executor without
    awaiting completion of the processing. Executor has to wait
    for the end of processing.
    """
    for repo in repos.values():
        executor.run(process_repo(repo))
