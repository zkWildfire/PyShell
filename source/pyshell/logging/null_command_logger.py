from pyshell.core.command_result import CommandResult
from pyshell.logging.command_logger import ICommandLogger
from pyshell.logging.stream_config import StreamConfig
from pyshell.scanners.entry import Entry
from typing import List, IO, Optional


class NullCommandLogger(ICommandLogger):
    """
    Logger that outputs nothing.
    @ingroup logging
    """
    def __init__(self,
        stream_config: StreamConfig = StreamConfig.MERGED_STREAMS) -> None:
        """
        Initializes the logger.
        @param stream_config The stream configuration the logger wants.
        """
        self._stream_config = stream_config


    @property
    def stream_config(self) -> StreamConfig:
        """
        Returns the stream configuration the logger wants.
        """
        return self._stream_config


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
        # Do nothing


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
        # Do nothing
