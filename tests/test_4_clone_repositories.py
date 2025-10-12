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

from autogit.actions._4_clone_repositories import (
    clone_repositories,
    clone_repository,
    get_repo_access_url,
    print_cloned_repositories,
)

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
        (
            'git@gitlab.com:niekas/jsonstate.git',
            'git@gitlab.com:niekas/jsonstate.git'
        ),

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


async def test_clone_repository():
    pass


def test_print_cloned_repositories():
    pass


def test_clone_repositories():
    pass
