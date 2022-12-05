from dataclasses import dataclass
from gitmultirepoupdater.constants import CloningStates


@dataclass
class RepoState:
    url: str  # Url used to clone the repository
    cloning_state: str = CloningStates.NOT_STARTED.value
