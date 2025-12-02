from dataclasses import dataclass

from autogit.constants import (
    BranchCreationState,
    CloningStates,
    ModificationState,
    PullRequestStates,
    PushToRemoteState,
)


@dataclass
class CliArguments:
    action_id: str  # Generated hash for action identification
    repos: list[str]  # A list of Urls or files containing Urls
    clone_to: str  # Directory which will be used to clone repos to
    commands: list[str]  # Commands which have to be exeucted in cloned repo
    commit_message: str  # Message which will be used for commit, branch, PR (if not provided)
    verbose: bool  # Provides additional debug information
    source_branch: (
        str | None
    )  # Base branch on which the new branch will be created (if it does not exist yet)
    branch: (
        str | None
    )  # Branch to use in PR as a source branch (it will be created if does not exist)
    target_branch: str | None  # Branch to use in PR as a target branch
    merge: bool  # Merge PR by skipping CI pipeline and other checks
    merge_on_success: bool  # Set auto merge flag that automatically merges the PR when CI pipeline succeeds


@dataclass
class RepoState:
    args: CliArguments  # Parsed command line arguments

    source_branch: str = ''  # Branch name from which a new branch for changes will be created
    branch: str = ''  # Branch name in which changes will be made and commited
    target_branch: str = ''  # Base branch into which PR changes will be pulled

    cloning_state: str = CloningStates.NOT_STARTED.value
    branch_creation_state: str = BranchCreationState.NOT_STARTED.value
    modification_state: str = ModificationState.NOT_STARTED.value
    push_to_remote_state: str = PushToRemoteState.NOT_STARTED.value
    pull_request_state: str = PullRequestStates.NOT_STARTED.value
    pull_request_status_code: int | None = None
    pull_request_reason: str | None = None

    name: str = ''  # Short human readable repo identifier
    owner: str = ''  # Owner of this repo
    path: str | None = ''  # project_id - Identifier of the repo: group/subgroup, owner and repo name
    url: str = ''  # Url used to clone the repository
    domain: str = ''  # Domain where the remote repository is hosted at (parsed from url)
    pull_request_url: str = ''  # Link to created pull request
    directory: str = ''  # Repository path in the file system
    exception_file_path: str = ''  # Repository path in the file system

    stdout: bytes = b''  # Standard output from command execution
    stderr: bytes = b''  # Standard error output from command execution

    @property
    def cloning_state_label(self) -> str:
        if self.cloning_state == CloningStates.NOT_STARTED.value:
            return ''
        if self.cloning_state == CloningStates.CLONING.value:
            return '⌛'
        if self.cloning_state == CloningStates.CLONED.value:
            return '✅ \033[1;32mCloned\033[0m'
        return f'❌ \033[1;33m{self.cloning_state.replace("_", " ").capitalize()}\033[0m'

    @property
    def branch_creation_state_label(self) -> str:
        if self.branch_creation_state == BranchCreationState.NOT_STARTED.value:
            return ''
        if self.branch_creation_state == BranchCreationState.CREATING.value:
            return '⌛ Applying changes'
        if self.branch_creation_state == BranchCreationState.CREATED.value:
            return '✅ \033[1;32mBranch created\033[0m'
        if self.branch_creation_state == BranchCreationState.SWITCHED_TO_EXISTING.value:
            return '✅ \033[1;32mSwitched to existing branch\033[0m'
        if self.branch_creation_state in [
            BranchCreationState.FAILED_TO_CREATE_BRANCH.value,
            BranchCreationState.FAILED_TO_PULL_CHANGES.value,
        ]:
            return f'❌ \033[1;33m{self.branch_creation_state.replace("_", " ").capitalize()}\033[0m'
        return f'❌ {self.branch_creation_state.replace("_", " ").capitalize()} Modification state display failure'

    @property
    def modification_state_label(self) -> str:  # noqa: PLR0911
        if self.modification_state == ModificationState.NOT_STARTED.value:
            return ''
        if self.modification_state == ModificationState.MODIFYING.value:
            return '⌛ Applying changes'
        if self.modification_state == ModificationState.MODIFIED.value:
            return '⌛ Applied changes'
        if self.modification_state == ModificationState.GOT_EXCEPTION.value:
            return f'❌ \033[1;33m{self.modification_state.replace("_", " ").capitalize()}\033[0m'
        return f'❌ {self.modification_state.replace("_", " ").capitalize()} Modification state display failure'

    @property
    def push_to_remote_state_label(self) -> str:
        state = self.push_to_remote_state.capitalize().replace('_', ' ')
        if self.push_to_remote_state == PushToRemoteState.NOT_STARTED.value:
            label = ''
        elif self.push_to_remote_state in [
            PushToRemoteState.COMMITING.value,
            PushToRemoteState.PUSHING_TO_REMOTE.value,
        ]:
            label = f'⌛ {state}'
        elif self.push_to_remote_state == PushToRemoteState.PUSHED_TO_REMOTE.value:
            label = f'✅ \033[1;32m{state}\033[0m'
        elif self.push_to_remote_state in [
            PushToRemoteState.NO_FILES_CHANGED.value,
            ModificationState.FAILED_TO_PUSH_TO_REMOTE.value,
        ]:
            label = f'❌ \033[1;33m{state}\033[0m'
        else:
            label = f'❌ {state} Modification state display failure'
        return label

    @property
    def pull_request_state_label(self) -> str:
        if self.pull_request_state == PullRequestStates.NOT_STARTED.value:
            return ''
        if self.pull_request_state == PullRequestStates.CREATING.value:
            return '⌛ Creating PR'
        if self.pull_request_state == PullRequestStates.CREATED.value:
            return '✅ \033[1;32mCreated PR\033[0m'
        if self.pull_request_state == PullRequestStates.MERGED.value:
            return '✅ \033[1;32mMerged PR\033[0m'
        if self.pull_request_state == PullRequestStates.SET_TO_AUTO_MERGE.value:
            return '✅ \033[1;32mPR Set to Auto Merge\033[0m'
        if self.pull_request_state == PullRequestStates.FAILED_TO_MERGE.value:
            return '❌ \033[1;32mFailed to Merge PR\033[0m'
        if self.pull_request_state == PullRequestStates.FAILED_TO_AUTO_MERGE.value:
            return '❌ \033[1;32mFailed to Auto-Merge PR\033[0m'
        if self.pull_request_state == PullRequestStates.GOT_BAD_RESPONSE.value:
            return f'❌ \033[1;33mPR {self.pull_request_state.replace("_", " ").capitalize()}\033[0m  {self.pull_request_status_code} {self.pull_request_reason}'
        return f'❌ {self.pull_request_state.replace("_", " ").capitalize()} PR state display failure'


@dataclass
class HttpRequestParams:
    url: str
    headers: dict[str, str]
    data: dict[str, str]
    json: dict[str, str] | None = None
