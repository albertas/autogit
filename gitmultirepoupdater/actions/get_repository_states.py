import logging
from urllib.parse import urlparse

import os
import os.path

from gitmultirepoupdater.data_types import CliArguments, RepoState
from gitmultirepoupdater.utils.helpers import get_access_token
from gitmultirepoupdater.utils.helpers import get_repo_name, get_repo_owner, get_domain

logger = logging.getLogger()


def is_url_or_git(file_names_or_repo_url: str) -> bool:
    # TODO: use urlparse to verify if its url and use regexp for git url
    return ".com" in file_names_or_repo_url.lower()


def read_repositories_from_file(repos_filename) -> list[str]:
    """Reads a list of repositories from a file while ignoring commented out lines."""
    with open(repos_filename) as f:
        return [l.strip() for l in f.readlines() if not l.strip().startswith("#")]


def standardize_git_repo_url(url: str) -> str:
    """Converts repository url to url which is suitable for cloning"""
    # https://gitlab.com/-/profile/personal_access_tokens
    # GITLAB_ACCESS_TOKEN
    # GITHUB_OAUTH_TOKEN
    # GIT_TOKEN

    # TODO: add github.com support
    if access_token := get_access_token(url):
        parsed_url = urlparse(url)
        domain_with_access_token = f"api:{access_token}@{parsed_url.netloc.split('@')[-1]}"
        parsed_url = parsed_url._replace(netloc=domain_with_access_token, scheme="https")
        return parsed_url.geturl()
    return url


def get_repository_states(args: CliArguments) -> dict[str, RepoState]:
    repo_urls = []
    for file_names_or_repo_url in args.repos:
        if not is_url_or_git(file_names_or_repo_url) and os.path.exists(file_names_or_repo_url):
            newly_read_repos = read_repositories_from_file(file_names_or_repo_url)
            repo_urls.extend(newly_read_repos)
        else:
            repo_urls.append(file_names_or_repo_url)

    repos: dict[str, RepoState] = {}
    for repo_url in repo_urls:
        standardized_repo_url = standardize_git_repo_url(repo_url)
        repo_name = get_repo_name(repo_url)
        repo_owner = get_repo_owner(repo_url)
        domain = get_domain(repo_url)
        repos[repo_name] = RepoState(
            args=args,
            name=repo_name,
            owner=repo_owner,
            url=standardized_repo_url,
            domain=domain
        )

    return repos
