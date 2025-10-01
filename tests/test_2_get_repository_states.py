import pytest

from autogit.actions._2_get_repository_states import get_repository_state


@pytest.mark.parametrize(
    ('repo_url', 'expected_name', 'expected_owner', 'expected_group', 'expected_domain'),
    [
        ('https://gitlab.com/myuser/myreponame.git', 'myreponame', 'myuser', None, 'gitlab.com'),
        (
            'https://managedgit.com/mygroup/mynamespace/myreponame',
            'myreponame',
            'mynamespace',
            'mygroup',
            'managedgit.com',
        ),
        (
            'https://managedgit.com/mygroup/mynamespace/myreponame.git',
            'myreponame',
            'mynamespace',
            'mygroup',
            'managedgit.com',
        ),
    ],
)
def test_get_repository_state(
    repo_url, expected_name, expected_owner, expected_group, expected_domain
):
    repo_state = get_repository_state(repo_url, 'tmp', None)
    assert repo_state.name == expected_name
    assert repo_state.owner == expected_owner
    assert repo_state.group == expected_group
    assert repo_state.domain == expected_domain
