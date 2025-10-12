import pytest

from autogit.data_types import CliArguments


@pytest.fixture
def action_id() -> str:
    return 'test_action_id'


@pytest.fixture
def repos() -> list[str]:
    return (['https://gitlab.com/myuser/myreponame.git'],)


@pytest.fixture
def clone_to() -> str:
    return 'tmp'


@pytest.fixture
def commands() -> list[str] | str:
    return ['echo', "'Hello'"]


@pytest.fixture
def commit_message() -> str:
    return 'Test commit message'


@pytest.fixture
def verbose() -> bool:
    return False


@pytest.fixture
def source_branch() -> str:
    return 'test_source_branch'


@pytest.fixture
def target_branch() -> str:
    return 'test_target_branch'


@pytest.fixture
def branch() -> str:
    return 'test_branch'


@pytest.fixture
def args(
    action_id,
    repos,
    clone_to,
    commands,
    commit_message,
    verbose,
    source_branch,
    branch,
    target_branch,
) -> CliArguments:
    return CliArguments(
        action_id=action_id,
        repos=repos,
        clone_to=clone_to,
        commands=commands,
        commit_message=commit_message,
        verbose=verbose,
        source_branch=source_branch,
        branch=branch,
        target_branch=target_branch,
    )
