from dataclasses import dataclass

from autogit.constants import CloningStates, ModificationState, PullRequestStates


@dataclass
class CliArguments:
    action_id: str  # Generated hash for action identification
    repos: list[str]  # A list of Urls or files containing Urls
    clone_to: str  # Directory which will be used to clone repos to
    commands: list[str]  # Commands which have to be exeucted in cloned repo
    commit_message: (
        str  # Message which will be used for commit, branch, PR (if not provided)
    )
    verbose: bool  # Provides additional debug information
    branch: str | None  # Branch name for newly created changes


@dataclass
class RepoState:
    args: CliArguments  # Parsed command line arguments

    source_branch: str = (
        ''  # Branch name from which a new branch for changes will be created
    )
    branch: str = ''  # Branch name in which changes will be made and commited
    target_branch: str = ''  # Base branch into which PR changes will be pulled

    cloning_state: str = CloningStates.NOT_STARTED.value
    modification_state: str = ModificationState.NOT_STARTED.value
    pull_request_state: str = PullRequestStates.NOT_CREATED.value
    pull_request_status_code: int | None = None
    pull_request_reason: str | None = None

    name: str = ''  # Short human readable repo identifier
    owner: str = ''  # Owner of this repo
    url: str = ''  # Url used to clone the repository
    domain: str = (
        ''  # Domain where the remote repository is hosted at (parsed from url)
    )
    pull_request_url: str = ''  # Link to created pull request
    directory: str = ''  # Repository path in the file system

    stdout: bytes = b''  # Standard output from command execution
    stderr: bytes = b''  # Standard error output from command execution


@dataclass
class HttpRequestParams:
    url: str
    headers: dict[str, str]
    data: dict[str, str]
    json: dict[str, str] | None = None
