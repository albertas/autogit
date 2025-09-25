from git.cmd import Git
import git

from autogit.data_types import RepoState
from autogit.utils.helpers import to_kebab_case
from autogit.utils.throttled_tasks_executor import ThrottledTasksExecutor


async def create_branch(repo: RepoState) -> None:
    if repo.args.branch:
        new_branch_name = repo.args.branch
    else:
        new_branch_name = (
            f'{to_kebab_case(repo.args.commit_message)}-{repo.args.action_id}'
        )
    repo.branch = new_branch_name

    g = Git(repo.directory)
    g.execute(['git', 'checkout', '-b', repo.branch])
    try:
        g.execute(['git', 'pull', 'origin', repo.branch])
    except git.exc.GitCommandError:
        print('Branch in the remote does not exist yet')


def create_branch_for_each_repo(
    repos: dict[str, RepoState], executor: ThrottledTasksExecutor
) -> None:
    for repo in repos.values():
        executor.run_not_throttled(create_branch(repo))
    executor.wait_for_tasks_to_finish()
