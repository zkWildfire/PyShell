from abc import ABC, abstractmethod
from nautilus.core.command import ICommand
from nautilus.core.command_result import CommandResult

class IErrorHandler(ABC):
    """
    Represents an error handler for Nautilus commands.
    """
    @abstractmethod
    def handle(self, command: ICommand, result: CommandResult) -> None:
        """
        Handles a command that returned a non-zero exit code.
        @param command Command that was run.
        @param result The result of the command.
        """
        raise NotImplementedError()
