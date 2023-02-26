from abc import ABC, abstractmethod
from pyshell.core.command_metadata import CommandMetadata
from pyshell.core.command_result import CommandResult

class IErrorHandler(ABC):
    """
    Represents an error handler for PyShell commands.
    @ingroup error
    """
    @abstractmethod
    def should_run(self, metadata: CommandMetadata) -> bool:
        """
        Whether the command should be allowed to run.
        @param metadata Metadata for the command about to be run.
        @returns True if the command should be allowed to run.
        """
        raise NotImplementedError()


    @abstractmethod
    def handle(self, result: CommandResult) -> None:
        """
        Handles a command that returned a non-zero exit code.
        @param result Data for the command that was run.
        """
        raise NotImplementedError()
