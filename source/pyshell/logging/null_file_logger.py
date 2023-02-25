from pyshell.core.command_result import CommandResult
from pyshell.logging.logger import ILogger

class NullFileLogger(ILogger):
    """
    Logger that does not log anything.
    """
    def log(self, result: CommandResult) -> None:
        """
        Writes the result of a command to a log file.
        @param result The result of the command.
        """
        # Do nothing
