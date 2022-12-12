import os
import subprocess

from gitmultirepoupdater.data_types import RepoState
from gitmultirepoupdater.utils.throttled_tasks_executor import ThrottledTasksExecutor


async def run_command(repo_state: RepoState) -> None:
    commands = repo_state.args.commands

    # Expand the name of the first argument if its a file and its in current directory
    if commands and os.path.exists(commands[0]) and os.path.isfile(commands[0]):
        commands[0] = os.path.abspath(commands[0])

    # Execute commands
    proc = subprocess.Popen(
        repo_state.args.commands,
        cwd=os.path.abspath(repo_state.repo_path),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    # TODO: Show output in real time:  https://stackoverflow.com/a/20576150
    stdout, stderr = proc.communicate()


def run_command_for_each_repo(repo_states: dict[str, RepoState], executor: ThrottledTasksExecutor) -> None:
    for repo_state in repo_states.values():
        executor.run_not_throttled(run_command(repo_state))
    executor.wait_for_tasks_to_finish()
