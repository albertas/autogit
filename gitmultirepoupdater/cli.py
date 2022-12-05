from typing import Optional
from gitmultirepoupdater.utils.argument_parsing import parse_command_line_arguments
from gitmultirepoupdater.actions.clone_repositories import clone_repositories, get_repository_states

# Should save state about each repository

def main(args: Optional[list[str]] = None) -> None:
    args = parse_command_line_arguments(args)
    repo_states = get_repository_states(file_names_or_repo_urls=args.repos)

    clone_repositories(repo_states, clone_to=args.clone_to)
    # create_branch(repo_states)
    # run_scripts_in_repo(repo_states, commands=args.commands)
    # commit_changes(repo_states)
    # push_commit(repo_states)
    # create_pull_request(repo_states)


if __name__ == "__main__":
    main()
