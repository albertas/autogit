from typing import Dict
import git
from git.cmd import Git

from gitmultirepoupdater.data_types import RepoState
from gitmultirepoupdater.utils.helpers import to_kebab_case, get_random_hex
from gitmultirepoupdater.utils.throttled_tasks_executor import ThrottledTasksExecutor


async def create_branch(repo: RepoState):
    if repo.args.branch:
        new_branch_name = repo.args.branch
    else:
        new_branch_name = f"{to_kebab_case(repo.args.commit_message)}-{get_random_hex()}"
    repo.branch = new_branch_name

    g = Git(repo.directory)
    g.execute(["git", "checkout", "-b", repo.branch])
    g.execute(["git", "pull", "origin", repo.branch])


def create_branch_for_each_repo(repos: Dict[str, RepoState], executor: ThrottledTasksExecutor) -> None:
    for repo in repos.values():
        executor.run_not_throttled(create_branch(repo))
    executor.wait_for_tasks_to_finish()
