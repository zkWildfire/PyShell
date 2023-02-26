from abc import abstractmethod
from pyshell.core.command_result import CommandResult
from pyshell.core.pyshell_component import IPyShellComponent
from pyshell.scanners.entry import Entry
from typing import List

class ILogger(IPyShellComponent):
    """
    Represents a logger for PyShell.
    Loggers are executed after a command is run regardless of the result of the
      command. This allows for logging of both successful and failed commands
      since the logger is executed before an error handler is called to handle
      a failed command.
    @ingroup logging
    """
    @abstractmethod
    def log(self,
        result: CommandResult,
        scanner_output: List[Entry]) -> None:
        """
        Writes the result of a command to a log file.
        @param result The result of the command.
        @param scanner_output The output of the scanner assigned to the command,
          if any.
        """
        raise NotImplementedError()
