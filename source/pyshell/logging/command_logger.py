from abc import ABC, abstractmethod
from pyshell.commands.command_result import CommandResult
from pyshell.logging.stream_config import StreamConfig
from pyshell.scanners.entry import Entry
from typing import List, IO, Optional

class ICommandLogger(ABC):
    """
    Base interface for loggers that handle a single command.
    PyShell will request a new command logger instance from the `ILogger` that
      the PyShell instance is configured with.
    @ingroup logging
    """
    @property
    @abstractmethod
    def stream_config(self) -> StreamConfig:
        """
        Returns the stream configuration the logger wants.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def output(self) -> str:
        """
        Returns the output of the command.
        This string must include both stdout and stderr output.
        """
        raise NotImplementedError()


    @abstractmethod
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
        raise NotImplementedError()


    @abstractmethod
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
        raise NotImplementedError()
