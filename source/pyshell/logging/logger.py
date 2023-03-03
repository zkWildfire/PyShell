from abc import abstractmethod
from pathlib import Path
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.core.pyshell_component import IPyShellComponent
from pyshell.logging.command_logger import ICommandLogger

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
        raise NotImplementedError()
