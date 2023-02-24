from abc import ABC, abstractmethod
from pyshell.core.command_result import CommandResult
from typing import Sequence

class IBackend(ABC):
    """
    Represents a backend for executing PyShell commands.
    """
    @abstractmethod
    def run(self, command: Sequence[str]) -> CommandResult:
        """
        Runs the specified command on the backend.
        @param command The command to run.
        @return The output of the command.
        """
        raise NotImplementedError()
