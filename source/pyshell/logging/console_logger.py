from pathlib import Path
from pyshell.core.command_metadata import CommandMetadata
from pyshell.logging.console_command_logger import ConsoleCommandLogger
from pyshell.logging.command_logger import ICommandLogger
from pyshell.logging.logger import ILogger

class ConsoleLogger(ILogger):
    """
    Logs all commands' output to the console.
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
        return ConsoleCommandLogger(metadata)
