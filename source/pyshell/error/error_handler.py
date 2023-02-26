from abc import abstractmethod
from pyshell.core.command_result import CommandResult
from pyshell.core.pyshell_component import IPyShellComponent

class IErrorHandler(IPyShellComponent):
    """
    Represents an error handler for PyShell commands.
    @ingroup error
    """
    @abstractmethod
    def handle(self, result: CommandResult) -> None:
        """
        Handles a command that returned a non-zero exit code.
        @param result Data for the command that was run.
        """
        raise NotImplementedError()
