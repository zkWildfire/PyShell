from pathlib import Path
from pyshell.core.command_result import CommandResult
from pyshell.logging.logger import ILogger

class NullFileLogger(ILogger):
    """
    Logger that does not log anything.
    """
    @property
    def file_path(self) -> Path:
        """
        Path to the file to write logs to. Will always be an absolute path.
        """
        return Path("/dev/null")


    def log(self, result: CommandResult) -> None:
        """
        Writes the result of a command to a log file.
        @param result The result of the command.
        """
        # Do nothing
