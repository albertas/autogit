import os
import subprocess

import aiofiles

from autogit.data_types import ModificationState, RepoState


async def run_command(repo: RepoState) -> bool:
    """Execute code modification CLI command provided by the user.

    :return: bool - was command executed successfully and code was modified.
    """
    repo.modification_state = ModificationState.MODIFYING.value
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
    # TODO: log the output in the temporal files.
    repo.stdout, repo.stderr = proc.communicate()

    if proc.returncode:
        repo.modification_state = ModificationState.GOT_EXCEPTION.value

        repo.exception_file_path = f"{repo.directory.rstrip('/')}_{repo.args.action_id}_error.txt"
        async with aiofiles.open(repo.exception_file_path, 'wb') as error_file:
            await error_file.write(repo.stdout)
            await error_file.write(b'\n\n')
            await error_file.write(repo.stderr)
    else:
        repo.modification_state = ModificationState.MODIFIED.value

    return repo.modification_state == ModificationState.MODIFIED.value
