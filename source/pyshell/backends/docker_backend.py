from pyshell.backends.backend import IBackend
from pyshell.core.command_result import CommandResult
from typing import Sequence

class DockerBackend(IBackend):
    """
    Backend that executes commands in a docker container.
    """

    def run(self, command: Sequence[str]) -> CommandResult:
        """
        Runs the specified command on the backend.
        @param command The command to run.
        @return The output of the command.
        """
        raise NotImplementedError()
