import os
from unittest.mock import patch

import pytest

from autogit.actions._4_clone_repositories import (
    get_repo_access_url,
)

# https://gitlab.com/niekas/jsonstate.git


@pytest.mark.parametrize(
    ('url', 'expected_url'),
    [
        (
            'https://gitlab.com/niekas/jsonstate.git',
            'https://api:<GITLAB_ACCESS_TOKEN>@gitlab.com/niekas/jsonstate.git',
        ),
        (
            'http://gitlab.com/niekas/jsonstate.git',
            'https://api:<GITLAB_ACCESS_TOKEN>@gitlab.com/niekas/jsonstate.git',
        ),
        (
            'https://github.com/niekas/jsonstate.git',
            'https://api:<GITHUB_OAUTH_TOKEN>@github.com/niekas/jsonstate.git',
        ),
        (
            'http://github.com/niekas/jsonstate.git',
            'https://api:<GITHUB_OAUTH_TOKEN>@github.com/niekas/jsonstate.git',
        ),
        ('git@gitlab.com:niekas/jsonstate.git', 'git@gitlab.com:niekas/jsonstate.git'),
    ],
)
def test_get_repo_access_url(url, expected_url):
    with patch.dict(
        os.environ,
        {
            'GITLAB_ACCESS_TOKEN': '<GITLAB_ACCESS_TOKEN>',
            'GITHUB_OAUTH_TOKEN': '<GITHUB_OAUTH_TOKEN>',
            'GIT_TOKEN': '<GIT_TOKEN>',
        },
    ):
        access_url = get_repo_access_url(url)
        assert access_url == expected_url
