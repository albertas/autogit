import git

from autogit.constants import ModificationState
from autogit.data_types import RepoState
from autogit.utils.throttled_tasks_executor import ThrottledTasksExecutor


async def commit_and_push_changes(repo: RepoState) -> None:
    g = git.Repo(repo.directory)

    if g.index.diff(None) or g.untracked_files:
        g.git.add(A=True)
        g.git.commit(m=repo.args.commit_message)

        g.git.push('--set-upstream', 'origin', repo.branch)
        repo.modification_state = ModificationState.PUSHED_TO_REMOTE.value
    else:
        repo.modification_state = ModificationState.NO_FILES_CHANGED.value
