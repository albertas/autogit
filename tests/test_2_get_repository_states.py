import pytest

from autogit.actions._2_get_repository_states import get_repository_state
from autogit.data_types import CliArguments


@pytest.mark.parametrize(
    ('repo_url', 'expected_name', 'expected_owner', 'expected_path', 'expected_domain'),
    [
        ('https://gitlab.com/myuser/myreponame.git', 'myreponame', 'myuser', 'myuser/myreponame', 'gitlab.com'),
        (
            'https://managedgit.com/mygroup/mynamespace/myreponame',
            'myreponame',
            'mynamespace',
            'mygroup/mynamespace/myreponame',
            'managedgit.com',
        ),
        (
            'https://managedgit.com/mygroup/mynamespace/myreponame.git',
            'myreponame',
            'mynamespace',
            'mygroup/mynamespace/myreponame',
            'managedgit.com',
        ),
        (
            'https://managedgit.com/mygroup/mysubgroup/mynamespace/myreponame.git',
            'myreponame',
            'mynamespace',
            'mygroup/mysubgroup/mynamespace/myreponame',
            'managedgit.com',
        ),
    ],
)
def test_get_repository_state(
    args, repo_url, expected_name, expected_owner, expected_path, expected_domain
):
    repo_state = get_repository_state(repo_url, args=args)
    assert repo_state.name == expected_name
    assert repo_state.owner == expected_owner
    assert repo_state.path == expected_path
    assert repo_state.domain == expected_domain


@pytest.fixture
def args():
    return CliArguments(
        action_id='test_action_id',
        repos=['https://gitlab.com/myuser/myreponame.git'],
        clone_to='tmp',
        commands=['echo', "'Hello'"],
        commit_message='Test commit message',
        verbose=False,
        source_branch='test_source_branch',
        branch='test_branch',
        target_branch='test target_branch',
    )
