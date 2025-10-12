import logging
import os
import os.path

from autogit.data_types import CliArguments, RepoState
from autogit.utils.helpers import (
    get_domain,
    get_repo_path,
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


def get_repository_state(
    repo_url: str,
    args: CliArguments = None,
) -> RepoState:
    repo_name = get_repo_name(repo_url)
    repo_owner = get_repo_owner(repo_url)
    repo_path = get_repo_path(repo_url)
    domain = get_domain(repo_url)

    return RepoState(
        args=args,
        name=repo_name,
        owner=repo_owner,
        path=repo_path,
        url=repo_url,
        domain=domain,
        source_branch=args.source_branch,
        branch=args.branch,
        target_branch=args.target_branch,
    )


def get_repository_states(args: CliArguments) -> dict[str, RepoState]:
    repo_urls = []
    for file_names_or_repo_url in args.repos:
        if not is_url_or_git(file_names_or_repo_url) and os.path.exists(file_names_or_repo_url):
            newly_read_repos = read_repositories_from_file(file_names_or_repo_url)
            repo_urls.extend(newly_read_repos)
        else:
            repo_urls.append(file_names_or_repo_url)

    if not args.branch:
        args.branch = to_kebab_case(args.commit_message)
        ## TODO: print this when verbosity is turned on
        # print(
        #     f'\033[1;32m|\033[0m {(f"New branch:  {args.branch}").ljust(75, " ")} \033[1;32m|\033[0m\n'
        # )

    repos: dict[str, RepoState] = {}
    for repo_url in repo_urls:
        repo_state = get_repository_state(
            repo_url=repo_url,
            args=args,
        )
        repos[repo_state.name] = repo_state

    return repos
