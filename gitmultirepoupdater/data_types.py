from dataclasses import dataclass
from gitmultirepoupdater.constants import CloningStates


@dataclass
class CliArguments:
    repos: list[str]
    clone_to: str
    commands: list[str]
    commit_message: str
    verbose: bool


@dataclass
class RepoState:
    args: CliArguments  # Parsed command line arguments 
    branch_name: str = ""  # Branch name in which changes should be made and commited
    cloning_state: str = CloningStates.NOT_STARTED.value
    repo_name: str = ""  # Short human readable repo identifier
    repo_url: str = ""  # Url used to clone the repository
    repo_path: str = ""
