import contextlib

import git
from git.cmd import Git

from autogit.constants import BranchCreationState
from autogit.data_types import RepoState
from autogit.utils.helpers import to_kebab_case


async def create_branch(repo: RepoState) -> bool:
    """Create branch in which code changes will be created.

    :return: bool - was branch created successfully.
    """
    repo.branch_creation_state = BranchCreationState.CREATING.value

    if repo.args.branch:
        new_branch_name = repo.args.branch
    else:
        new_branch_name = to_kebab_case(repo.args.commit_message)
        if repo.args.action_id and repo.args.action_id not in new_branch_name:
            new_branch_name += f'-{repo.args.action_id}'

    repo.branch = new_branch_name

    g = Git(repo.directory)

    # TODO: add a conditional check if the branch exists or not
    # TODO: what should be done if the branch exists and contains changes? Error should be shown and action canceled with nice error message.
    try:
        g.execute(['git', 'checkout', '-b', repo.branch])
        repo.branch_creation_state = BranchCreationState.CREATED.value
    except git.exc.GitCommandError:
        try:
            g.execute(['git', 'checkout', repo.branch])
            repo.branch_creation_state = BranchCreationState.SWITCHED_TO_EXISTING.value
        except git.exc.GitCommandError:
            repo.branch_creation_state = BranchCreationState.FAILED_TO_CREATE_BRANCH.value

    with contextlib.suppress(git.exc.GitCommandError):
        try:
            g.execute(['git', 'pull', 'origin', repo.branch])
        except git.exc.GitCommandError:
            repo.branch_creation_state = BranchCreationState.FAILED_TO_PULL_CHANGES.value

    return repo.branch_creation_state in [
        BranchCreationState.CREATED.value,
        BranchCreationState.SWITCHED_TO_EXISTING.value,
    ]
