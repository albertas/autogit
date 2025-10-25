from pathlib import Path
from urllib.parse import urlparse

import git
from git.cmd import Git
from git.exc import GitCommandError

from autogit.actions._4_show import show_failure
from autogit.constants import CloningStates
from autogit.data_types import RepoState
from autogit.utils.helpers import get_access_token, get_default_branch


def get_repo_access_url(url: str) -> str | None:
    """Converts repository url to url which is suitable for cloning."""
    if url.startswith('http'):
        if access_token := get_access_token(url):
            parsed_url = urlparse(url)
            domain_with_access_token = f'api:{access_token}@{parsed_url.netloc.split("@")[-1]}'
            parsed_url = parsed_url._replace(netloc=domain_with_access_token, scheme='https')
            return parsed_url.geturl()
    elif url.startswith('git@'):
        return url
    return None


async def clone_repository(repo: RepoState) -> bool:
    """Clones repository with default (or source) branch.

    :return: bool - was repo cloned successfully.
    """
    repo.cloning_state = CloningStates.CLONING.value

    clone_to = repo.args.clone_to
    repo.directory = str((Path(clone_to) / repo.name).expanduser())

    # TODO: add a way to clone using access token: https://stackoverflow.com/questions/25409700/using-gitlab-token-to-clone-without-authentication/29570677#29570677
    # git clone https://:YOURKEY@your.gilab.company.org/group/project.git

    # TODO: add ssh support: urls like git@gitlab.com:niekas/gitlab-api-tests.git

    try:
        directory = Path(repo.directory)
        if directory.exists():
            ## TODO: check if directory exist
            if list(directory.iterdir()) and not (Path(repo.directory) / '.git/').exists():
                show_failure(
                    f'This is not a Git directory (wanted to clone to it): {repo.directory}'
                )
                repo.cloning_state = CloningStates.DIRECTORY_NOT_EMPTY.value
                return False

            # If repository exists: clean it, pull changes, checkout default branch
            g: Git = Git(repo.directory)
            g.clean('-dfx')
            g.execute(['git', 'fetch', '--all'])

            repo.target_branch = repo.target_branch or get_default_branch(repo)
            repo.source_branch = repo.source_branch or repo.target_branch

            g.checkout(repo.source_branch)

            repo.cloning_state = CloningStates.CLONED.value
        elif repo_access_url := get_repo_access_url(repo.url):
            Path(repo.directory).mkdir(parents=True)
            git.Repo.clone_from(url=repo_access_url, to_path=repo.directory)

            g = Git(repo.directory)
            g.execute(['git', 'fetch', '--all'])

            repo.target_branch = repo.target_branch or get_default_branch(repo)
            repo.source_branch = repo.source_branch or repo.target_branch

            try:
                g.checkout(repo.source_branch)
            except git.exc.GitCommandError:
                repo.cloning_state = CloningStates.SOURCE_BRANCH_DOES_NOT_EXIST.value
            else:
                repo.cloning_state = CloningStates.CLONED.value
        else:
            repo.cloning_state = CloningStates.ACCESS_TOKEN_NOT_PROVIDED.value

        return repo.cloning_state == CloningStates.CLONED.value  # noqa: TRY300

    except GitCommandError:
        repo.cloning_state = CloningStates.NOT_FOUND.value
