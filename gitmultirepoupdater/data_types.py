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
    source_branch: str = ""  # Branch name from which a new branch for changes will be created
    branch: str = ""  # Branch name in which changes will be made and commited
    target_branch: str = ""  # Base branch into which PR changes will be pulled into
    cloning_state: str = CloningStates.NOT_STARTED.value
    name: str = ""  # Short human readable repo identifier
    url: str = ""  # Url used to clone the repository
    directory: str = ""  # Repository path in the file system
    owner: str = ""  # Owner of this repo
