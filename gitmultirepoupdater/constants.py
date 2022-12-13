from enum import Enum


ACCESS_TOKEN_VAR_NAMES = {
    "gitlab.com": "GITLAB_ACCESS_TOKEN",
    "github.com": "GITHUB_OAUTH_TOKEN",
    "DEFAULT": "GIT_TOKEN",
}


class CloningStates(Enum):
    NOT_STARTED = "NOT_STARTED"
    CLONING = "CLONING"
    CLONED = "CLONED"
    NOT_FOUND = "NOT_FOUND"
    SKIPPED = "SKIPPED"


class PullRequestStates(Enum):
    NOT_CREATED = "NOT_CREATED"
    CREATED = "CREATED"
    MERGED = "MERGED"
