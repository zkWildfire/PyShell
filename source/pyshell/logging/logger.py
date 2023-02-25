from abc import ABC, abstractmethod
from pyshell.core.command_result import CommandResult

class ILogger(ABC):
    """
    Represents a logger for PyShell.
    Loggers are executed after a command is run regardless of the result of the
      command. This allows for logging of both successful and failed commands
      since the logger is executed before an error handler is called to handle
      a failed command.
    @ingroup logging
    """
    @abstractmethod
    def log(self, result: CommandResult) -> None:
        """
        Writes the result of a command to a log file.
        @param command Command that was run.
        @param result The result of the command.
        """
        raise NotImplementedError()
