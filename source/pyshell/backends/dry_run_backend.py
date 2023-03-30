from datetime import datetime
from pathlib import Path
from pyshell.backends.backend import IBackend
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.command_result import CommandResult
from pyshell.commands.sync_command_result import SyncCommandResult
from pyshell.logging.command_logger import ICommandLogger
from typing import List

class DryRunBackend(IBackend):
    """
    Backend that prints commands without executing them.
    @ingroup backends
    """
    def __init__(self):
        """
        Initializes the backend.
        """
        super().__init__()

        # List of commands that have been run.
        self._commands: List[str] = []


    @property
    def commands(self) -> List[str]:
        """
        The list of commands that have been run.
        """
        return self._commands


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
        print(metadata.full_command)
        self._commands.append(metadata.full_command)

        return SyncCommandResult(
            command=metadata.command,
            args=metadata.args,
            cwd=str(cwd),
            output="",
            exit_code=0,
            skipped=False,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow(),
            backend="Dry Run backend"
        )
