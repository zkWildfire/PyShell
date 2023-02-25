from pathlib import Path
from pyshell.backends.backend import IBackend
from pyshell.core.command_result import CommandResult
from typing import Sequence

class DryRunBackend(IBackend):
    """
    Backend that prints commands without executing them.
    @ingroup backends
    """
    def run(self,
        command: Sequence[str],
        cwd: Path) -> CommandResult:
        """
        Runs the specified command on the backend.
        @param command The command to run.
        @param cwd The working directory to use for the command. Will always be
          an absolute path.
        @return The output of the command.
        """
        full_cmd = " ".join(command)
        print(full_cmd)

        return CommandResult(
            command=command[0],
            args=command[1:],
            cwd=str(cwd),
            output="",
            exit_code=0
        )
