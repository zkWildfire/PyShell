from pyshell.backends.backend import IBackend
from pyshell.core.command_result import CommandResult
from typing import Sequence

class DryRunBackend(IBackend):
    """
    Backend that prints commands without executing them.
    """
    def run(self, command: Sequence[str]) -> CommandResult:
        """
        Runs the specified command on the backend.
        @param command The command to run.
        @return The output of the command.
        """
        full_cmd = " ".join(command)
        print(full_cmd)

        return CommandResult(
            command=command[0],
            args=command[1:],
            full_command=full_cmd,
            output="",
            exit_code=0,
            success=True
        )
