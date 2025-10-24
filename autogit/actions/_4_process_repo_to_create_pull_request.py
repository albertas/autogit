"""
This file aims to provide async function
for processing a single repository to create Pull Request.
The processing of a repository consists of these steps:
- Clone repository
- Create branch
- Run command
- Commit changes
- Push changes to the remote repository
- Create Pull Request
"""

from autogit.actions._4a_clone_repositories import clone_repository
from autogit.actions._4b_create_branch import create_branch
from autogit.actions._4c_run_command import run_command
from autogit.actions._4d_commit_and_push_changes import commit_and_push_changes
from autogit.actions._4e_create_pull_request import create_pull_request
from autogit.data_types import RepoState


async def process_repo(repo: RepoState) -> None:
    await clone_repository(repo)
    await create_branch(repo)
    await run_command(repo)
    await commit_and_push_changes(repo)
    await create_pull_request(repo)


async def start_repos_processing_to_create_pull_requests(
    repos: dict[str, RepoState], executor: ThrottledTasksExecutor
) -> None:
    """
    Submit repositories to be processed in executor without
    awaiting completion of the processing. Executor has to wait
    for the end of processing.
    """
    for repo in repos.values():
        executor.run(process_repo(repo))
