from pyshell.core.command_result import CommandResult
from pyshell.logging.logger import ILogger
from pyshell.scanners.entry import Entry
from typing import List

class NullFileLogger(ILogger):
    """
    Logger that does not log anything.
    @ingroup logging
    """
    def log(self,
        result: CommandResult,
        scanner_output: List[Entry]) -> None:
        """
        Writes the result of a command to a log file.
        @param result The result of the command.
        @param scanner_output The output of the scanner assigned to the command,
          if any.
        """
        # Do nothing
