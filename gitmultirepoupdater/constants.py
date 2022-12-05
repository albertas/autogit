from enum import Enum


class CloningStates(Enum):
    NOT_STARTED = "NOT_STARTED"
    CLONING = "CLONING"
    CLONED = "CLONED"
    NOT_FOUND = "NOT_FOUND"
    SKIPPED = "SKIPPED"
