import logging
import os
import os.path

from autogit.data_types import CliArguments, RepoState
from autogit.utils.helpers import (
    get_domain,
    get_repo_name,
    get_repo_owner,
    to_kebab_case,
)

logger = logging.getLogger()


def is_url_or_git(file_names_or_repo_url: str) -> bool:
    # TODO: use urlparse to verify if its url and use regexp for git url
    return '.com' in file_names_or_repo_url.lower()


def read_repositories_from_file(repos_filename: str) -> list[str]:
    """Reads a list of repositories from a file while ignoring commented out lines."""
    with open(repos_filename) as f:
        return [line.strip() for line in f if not line.strip().startswith('#')]


def get_repository_states(args: CliArguments) -> dict[str, RepoState]:
    repo_urls = []
    for file_names_or_repo_url in args.repos:
        if not is_url_or_git(file_names_or_repo_url) and os.path.exists(
            file_names_or_repo_url
        ):
            newly_read_repos = read_repositories_from_file(file_names_or_repo_url)
            repo_urls.extend(newly_read_repos)
        else:
            repo_urls.append(file_names_or_repo_url)

    branch = args.branch or to_kebab_case(args.commit_message)

    repos: dict[str, RepoState] = {}
    for repo_url in repo_urls:
        repo_name = get_repo_name(repo_url)
        repo_owner = get_repo_owner(repo_url)
        domain = get_domain(repo_url)

        repos[repo_name] = RepoState(
            args=args,
            name=repo_name,
            owner=repo_owner,
            url=repo_url,
            domain=domain,
            branch=branch,
        )

    return repos
