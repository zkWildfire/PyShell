from pathlib import Path
from pyshell.core.command_metadata import CommandMetadata
from pyshell.logging.command_logger import ICommandLogger
from pyshell.logging.logger import ILogger
from pyshell.logging.null_command_logger import NullCommandLogger

class NullLogger(ILogger):
    """
    Represents a logger for PyShell.
    Loggers are executed after a command is run regardless of the result of the
      command. This allows for logging of both successful and failed commands
      since the logger is executed before an error handler is called to handle
      a failed command.
    @ingroup logging
    """
    def construct_logger(self,
        metadata: CommandMetadata,
        cwd: Path) -> ICommandLogger:
        """
        Constructs a new command logger.
        @param metadata The metadata of the command that will the command logger
          will be used for.
        @param cwd The current working directory of the command that will the
          command logger will be used for.
        @return A new command logger instance.
        """
        return NullCommandLogger()
