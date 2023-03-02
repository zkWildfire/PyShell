from pyshell.core.command_flags import CommandFlags
from pyshell.core.command_metadata import CommandMetadata
from pyshell.core.command_result import CommandResult
from pyshell.logging.command_logger import ICommandLogger
from pyshell.logging.stream_config import StreamConfig
from pyshell.scanners.entry import Entry
from typing import List, IO, Optional


class ConsoleCommandLogger(ICommandLogger):
    """
    Logger that writes command output to the console.
    """
    def __init__(self, metadata: CommandMetadata) -> None:
        """
        Initializes the logger.
        @param metadata The metadata of the command being run.
        """
        self._metadata = metadata

        # Check whether the command's output shouldn't be logged
        self._skip_logging = False
        self._skip_logging &= metadata.flags & CommandFlags.QUIET
        self._skip_logging &= metadata.flags & CommandFlags.NO_CONSOLE


    @property
    def stream_config(self) -> StreamConfig:
        """
        Returns the stream configuration the logger wants.
        """
        return StreamConfig.MERGED_STREAMS


    def log(self,
        stdout: IO[str],
        stderr: Optional[IO[str]]) -> None:
        """
        Handles logging for a command being executed.
        This method will be invoked repeatedly until the command finishes and
          all output has been sent to the logger.
        @param stdout The stdout stream of the command.
        @param stderr The stderr stream of the command. If the logger requests
          that the stderr stream be merged with the stdout stream, this will be
          `None`.
        """
        if self._skip_logging:
            return

        print(stdout.read())


    def log_results(self,
        result: CommandResult,
        scanner_output: List[Entry]) -> None:
        """
        Logs the results of a command that finished executing.
        This method is guaranteed to be executed for every command. Command
          loggers should handle any cleanup in this method.
        @param result The result of the command that finished executing.
        @param scanner_output The output of the scanner assigned to the command,
          if any.
        """
        print(f"Command exited with code {result.exit_code}.")
        print(f"Note: Command was '{result.full_command}'.")
