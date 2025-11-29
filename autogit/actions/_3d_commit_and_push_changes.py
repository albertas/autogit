import git

from autogit.constants import PushToRemoteState
from autogit.data_types import RepoState


async def commit_and_push_changes(repo: RepoState) -> bool:
    """Commits and pushes changes to the remote repository.

    :return: bool - were changes commited and pushed to the remote repository.
    """
    repo.push_to_remote_state = PushToRemoteState.COMMITING.value

    g = git.Repo(repo.directory)

    if g.index.diff(None) or g.untracked_files:
        g.git.add(A=True)
        g.git.commit(m=repo.args.commit_message)
        repo.push_to_remote_state = PushToRemoteState.PUSHING_TO_REMOTE.value

        g.git.push('--set-upstream', 'origin', repo.branch)
        repo.push_to_remote_state = PushToRemoteState.PUSHED_TO_REMOTE.value
    else:
        repo.push_to_remote_state = PushToRemoteState.NO_FILES_CHANGED.value
    return repo.push_to_remote_state == PushToRemoteState.PUSHED_TO_REMOTE.value
