from logging import getLogger
from urllib.parse import urlparse
import os.path

import git

from gitmultirepoupdater.data_types import RepoState
from gitmultirepoupdater.constants import CloningStates

logger = getLogger()


def is_url_or_git(file_names_or_repo_url: str) -> bool:
    # TODO: use urlparse to verify if its url and use regexp for git url
    return ".com" in file_names_or_repo_url.lower()


def read_repositories_from_file(repos_filename) -> list[str]:
    with open(repos_filename) as f:
        return f.read().split()
    

def standardize_git_repo_url(url: str) -> str:
    """Converts repository url to url which is suitable for cloning"""
    parsed_url = urlparse(url)

    if access_token := os.getenv("GITLAB_ACCESS_TOKEN", ""):
        domain_with_access_token = f"api:{access_token}@{parsed_url.netloc}"
        parsed_url = parsed_url._replace(netloc=domain_with_access_token)

    return parsed_url.geturl()


def get_repository_states(file_names_or_repo_urls: list[str]) -> dict[str, RepoState]:
    repo_urls = []
    for file_names_or_repo_url in file_names_or_repo_urls:
        if not is_url_or_git(file_names_or_repo_url) and os.path.exists(file_names_or_repo_url):
            newly_read_repos = read_repositories_from_file(file_names_or_repo_url)
            repo_urls.extend(newly_read_repos)
        else:
            repo_urls.append(file_names_or_repo_url)

    repo_states = {}
    for repo_url in repo_urls:
        standardized_repo_url = standardize_git_repo_url(repo_url)
        repo_states[repo_url] = RepoState(url=standardized_repo_url)

    return repo_states


def clone_repository(repo_url: str, clone_to: str, repo_state: RepoState) -> None:
    repo_path = os.path.join(clone_to, repo_url.split("/")[-1])

    try:
        git.Repo.clone_from(repo_url, repo_path)
        repo_state.cloning_state = CloningStates.CLONED.value

        logger.debug(f"Cloned repo from {repo_url} to {clone_to}")

    except git.exc.GitCommandError:
        repo_state.cloning_state = CloningStates.NOT_FOUND.value


def clone_repositories(repo_states: dict[str, RepoState], clone_to: str) -> None:
    for repo_url, repo_state in repo_states.items():
        clone_repository(repo_state.url, clone_to, repo_state)
