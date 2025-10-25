from enum import Enum

ACCESS_TOKEN_VAR_NAMES = {
    'gitlab.com': 'GITLAB_ACCESS_TOKEN',
    'github.com': 'GITHUB_OAUTH_TOKEN',
    'DEFAULT': 'GIT_TOKEN',
}


class CloningStates(Enum):
    NOT_STARTED = 'NOT_STARTED'
    CLONING = 'CLONING'
    CLONED = 'CLONED'
    SOURCE_BRANCH_DOES_NOT_EXIST = 'SOURCE_BRANCH_DOES_NOT_EXIST'
    ACCESS_TOKEN_NOT_PROVIDED = 'ACCESS_TOKEN_NOT_PROVIDED'
    NOT_FOUND = 'NOT_FOUND'
    SKIPPED = 'SKIPPED'
    DIRECTORY_NOT_EMPTY = 'DIRECTORY_NOT_EMPTY'


class BranchCreationState(Enum):
    NOT_STARTED = 'NOT_STARTED'  # Initial
    CREATING = 'CREATING'  # Pending
    CREATED = 'CREATED'  # Good
    SWITCHED_TO_EXISTING = 'SWITCHED_TO_EXISTING'  # Good
    FAILED_TO_CREATE_BRANCH = 'FAILED_TO_CREATE_BRANCH'  # Bad
    FAILED_TO_PULL_CHANGES = 'FAILED_TO_PULL_CHANGES'  # Bad


class ModificationState(Enum):
    NOT_STARTED = 'NOT_STARTED'  # Initial
    MODIFYING = 'MODIFYING'  # Pending
    MODIFIED = 'MODIFIED'  # Good
    GOT_EXCEPTION = 'GOT_EXCEPTION'  # Bad


class PushToRemoteState(Enum):
    # TODO: should have separate state for pushing to remote states
    NOT_STARTED = 'NOT_STARTED'  # Initial
    COMMITING = 'COMMITING'  # Pending
    PUSHING_TO_REMOTE = 'PUSHING_TO_REMOTE'  # Pending
    PUSHED_TO_REMOTE = 'PUSHED_TO_REMOTE'  # Good
    NO_FILES_CHANGED = 'NO_FILES_CHANGED'  # Bad
    FAILED_TO_PUSH_TO_REMOTE = 'FAILED_TO_PUSH_TO_REMOTE'  # Bad


class PullRequestStates(Enum):
    NOT_STARTED = 'NOT_STARTED'  # Initial
    CREATING = 'CREATING'  # Pending
    CREATED = 'CREATED'  # Good
    GOT_BAD_RESPONSE = 'GOT_BAD_RESPONSE'  # Bad
    NOT_CREATED = 'NOT_CREATED'  # Bad
    MERGED = 'MERGED'  # Good
