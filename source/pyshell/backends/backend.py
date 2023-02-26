from abc import abstractmethod
from pathlib import Path
from pyshell.core.command_result import CommandResult
from pyshell.core.pyshell_component import IPyShellComponent
from typing import Sequence

class IBackend(IPyShellComponent):
    """
    Represents a backend for executing PyShell commands.
    @ingroup backends
    """
    @abstractmethod
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
        raise NotImplementedError()
