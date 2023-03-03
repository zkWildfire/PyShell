from abc import abstractmethod
from pathlib import Path
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.command_result import CommandResult
from pyshell.core.pyshell_component import IPyShellComponent
from pyshell.logging.command_logger import ICommandLogger

class IBackend(IPyShellComponent):
    """
    Represents a backend for executing PyShell commands.
    @ingroup backends
    """
    @abstractmethod
    def run(self,
        metadata: CommandMetadata,
        cwd: Path,
        logger: ICommandLogger) -> CommandResult:
        """
        Runs the specified command on the backend.
        @param metadata Metadata for the command to run.
        @param cwd The working directory to use for the command. Will always be
          an absolute path.
        @param logger The logger to use for the command. The backend will invoke
          `logger.log()` but will not invoke `logger.log_results()`.
        @return The output of the command.
        """
        raise NotImplementedError()
