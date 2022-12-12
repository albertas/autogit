from typing import Optional
from gitmultirepoupdater.actions.argument_parsing import parse_command_line_arguments
from gitmultirepoupdater.actions.get_repository_states import get_repository_states
from gitmultirepoupdater.actions.clone_repositories import clone_repositories
from gitmultirepoupdater.actions.create_branch import create_branch_for_each_repo
from gitmultirepoupdater.actions.run_command import run_command_for_each_repo
from gitmultirepoupdater.actions.commit_and_push_changes import commit_and_push_changes_for_each_repo 
from gitmultirepoupdater.actions.create_pull_request import create_pull_request_for_each_repo
from gitmultirepoupdater.utils.throttled_tasks_executor import ThrottledTasksExecutor

# Should save state about each repository

def main(args: Optional[list[str]] = None) -> None:
    args = parse_command_line_arguments(args)
    repo_states = get_repository_states(args)

    with ThrottledTasksExecutor(delay_between_tasks=0.2) as executor:
        clone_repositories(repo_states, executor)
        create_branch_for_each_repo(repo_states, executor)
        run_command_for_each_repo(repo_states, executor)
        commit_and_push_changes_for_each_repo(repo_states, executor)
        create_pull_request_for_each_repo(repo_states, executor)


if __name__ == "__main__":
    main()
