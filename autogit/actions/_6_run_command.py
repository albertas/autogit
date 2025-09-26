import os
import subprocess

from autogit.data_types import ModificationState, RepoState
from autogit.utils.throttled_tasks_executor import ThrottledTasksExecutor


async def run_command(repo: RepoState) -> None:
    commands = repo.args.commands

    # Expand the name of the first argument if its a file and its in current directory
    if commands and os.path.exists(commands[0]) and os.path.isfile(commands[0]):
        commands[0] = os.path.abspath(commands[0])

    # Execute commands
    proc = subprocess.Popen(
        repo.args.commands,
        cwd=os.path.abspath(repo.directory),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    # TODO: Show output in real time:  https://stackoverflow.com/a/20576150
    repo.stdout, repo.stderr = proc.communicate()
    if proc.returncode:
        repo.modification_state = ModificationState.GOT_EXCEPTION.value
    else:
        repo.modification_state = ModificationState.MODIFIED.value


def run_command_for_each_repo(
    repos: dict[str, RepoState], executor: ThrottledTasksExecutor
) -> None:
    for repo in repos.values():
        executor.run_not_throttled(run_command(repo))
    executor.wait_for_tasks_to_finish()
