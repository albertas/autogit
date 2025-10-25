"""
Tests that test clone repository for various scenarios.

I badly need manual testing with real API. Lets just do it.

  > Create a fixture that sets up real repository.
  > Mock the behavior of the real repository locally.
    > API changes so I should better have real repositories to test.

"""

import os
from unittest.mock import patch

import pytest

from autogit.actions._3a_clone_repositories import (
    clone_repository,
    get_repo_access_url,
)
from autogit.constants import CloningStates
from autogit.data_types import CliArguments, RepoState

## Methods to test:
# def get_repo_access_url(url: str) -> str | None:
# async def clone_repository(repo: RepoState) -> None:
# def print_cloned_repositories(repos):
# def clone_repositories(repos: dict[str, RepoState], executor: ThrottledTasksExecutor) -> None:


@pytest.mark.parametrize(
    ('repo_url', 'expected_access_url'),
    [
        # Gitlab repos
        (
            'https://gitlab.com/myuser/myreponame.git',
            'https://api:<GITLAB_ACCESS_TOKEN>@gitlab.com/myuser/myreponame.git',
        ),
        (
            'https://gitlab.com/mygroup/myuser/myreponame.git',
            'https://api:<GITLAB_ACCESS_TOKEN>@gitlab.com/mygroup/myuser/myreponame.git',
        ),
        ('git@gitlab.com:myusername/myreponame.git', 'git@gitlab.com:myusername/myreponame.git'),
        # Managed repos
        (
            'https://managedgit.com/myuser/myreponame',
            'https://api:<GIT_TOKEN>@managedgit.com/myuser/myreponame',
        ),
        (
            'https://managedgit.com/mygroup/mynamespace/myreponame',
            'https://api:<GIT_TOKEN>@managedgit.com/mygroup/mynamespace/myreponame',
        ),
        (
            'https://managedgit.com/mygroup/mynamespace/myreponame.git',
            'https://api:<GIT_TOKEN>@managedgit.com/mygroup/mynamespace/myreponame.git',
        ),
        (
            'https://managedgit.com/mygroup/mysubgroup/mynamespace/myreponame.git',
            'https://api:<GIT_TOKEN>@managedgit.com/mygroup/mysubgroup/mynamespace/myreponame.git',
        ),
        # Github repos
        (
            'https://github.com/myuser/reponame.git',
            'https://api:<GITHUB_OAUTH_TOKEN>@github.com/myuser/reponame.git',
        ),
        (
            'http://github.com/group/myuser/reponame.git',
            'https://api:<GITHUB_OAUTH_TOKEN>@github.com/group/myuser/reponame.git',
        ),
    ],
)
def test_get_repo_access_url(repo_url, expected_access_url):
    with patch.dict(
        os.environ,
        {
            'GITLAB_ACCESS_TOKEN': '<GITLAB_ACCESS_TOKEN>',
            'GITLAB_OAUTH_TOKEN': '<GITLAB_OAUTH_TOKEN>',
            'GITLAB_TOKEN': '<GITLAB_TOKEN>',
            'GITHUB_OAUTH_TOKEN': '<GITHUB_OAUTH_TOKEN>',
            'GITHUB_ACCESS_TOKEN': '<GITHUB_ACCESS_TOKEN>',
            'GITHUB_TOKEN': '<GITHUB_TOKEN>',
            'GIT_TOKEN': '<GIT_TOKEN>',
            'GIT_ACCESS_TOKEN': '<GIT_ACCESS_TOKEN>',
            'GIT_OAUTH_TOKEN': '<GIT_OAUTH_TOKEN>',
        },
    ):
        access_url = get_repo_access_url(repo_url)
        assert access_url == expected_access_url


@pytest.mark.parametrize(
    (
        'source_branch',
        'target_branch',
        'branch',
        'default_branch',
    ),
    [
        # Various branches exist/not when all branch names provided
        ('source', 'target', 'branch', 'main'),
        ('source_exists', 'target', 'branch', 'main'),
        ('source', 'target_exists', 'branch', 'main'),
        ('source', 'target', 'branch_exists', 'main'),
        ('source', 'target_exists', 'branch_exists', 'main'),
        ('source_exists', 'target', 'branch_exists', 'main'),
        ('source_exists', 'target_exists', 'branch', 'main'),
        ('source_exists', 'target_exists', 'branch_exists', 'main'),
        # Various branches exist/not when target branch name not provided
        ('source', None, 'branch', 'main'),
        ('source_exists', None, 'branch', 'main'),
        ('source', None, 'branch_exists', 'main'),
        ('source_exists', None, 'branch_exists', 'main'),
        # Various branches exist/not when target branch name not provided
        (None, 'target', 'branch', 'main'),
        (None, 'target_exists', 'branch', 'main'),
        (None, 'target', 'branch_exists', 'main'),
        (None, 'target_exists', 'branch_exists', 'main'),
        # Various branches exist/not when branch name not provided
        ('source', 'target', None, 'main'),
        ('source_exists', 'target', None, 'main'),
        ('source', 'target_exists', None, 'main'),
        ('source_exists', 'target_exists', None, 'main'),
        # Various branches exist/not when source/target branch names are not provided
        (None, None, 'branch', 'main'),
        (None, None, 'branch_exists', 'main'),
        # Various branches exist/not when only target branch provided
        (None, 'target', None, 'main'),
        (None, 'target_exists', None, 'main'),
        # Various branches exist/not when only source branch provided
        ('source', None, None, 'main'),
        ('source_exists', None, None, 'main'),
        # Various branches exist/not when no branch names are provided
        (None, None, None, 'main'),
    ],
)
async def test_clone_repository(
    args: CliArguments,
    repo: RepoState,
    remove_test_dir,
    source_branch,
    target_branch,
    branch,
    default_branch,
):
    # TODO: Should define fixtures that setup and clean Git repositories based on experiment result.
    with patch('autogit.actions._4_clone_repositories.Path.exists', return_value=False):
        # Could run it once in a ThrottledTasksExecutor and Mock Git later on.
        await clone_repository(repo)
        if source_branch == 'source' or (source_branch is None and target_branch == 'target'):
            # Source branch does not exist - cannot use it as basis
            assert repo.cloning_state == CloningStates.SOURCE_BRANCH_DOES_NOT_EXIST.value
        else:
            assert repo.cloning_state == CloningStates.CLONED.value


def test_print_cloned_repositories():
    pass


def test_clone_repositories():
    pass
