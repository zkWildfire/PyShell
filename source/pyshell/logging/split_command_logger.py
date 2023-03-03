from io import StringIO
from pyshell.core.command_result import CommandResult
from pyshell.logging.command_logger import ICommandLogger
from pyshell.logging.stream_config import StreamConfig
from pyshell.scanners.entry import Entry
from typing import List, IO, Optional

class SplitCommandLogger(ICommandLogger):
    """
    Command logger that writes each stream's output separately.
    @ingroup logging
    """
    def __init__(self,
        stdout_logger: ICommandLogger,
        stderr_logger: ICommandLogger) -> None:
        """
        Initializes the logger.
        @param stdout_logger The logger to use for stdout.
        @param stderr_logger The logger to use for stderr.
        """
        self._stdout_logger = stdout_logger
        self._stderr_logger = stderr_logger

        # Stores all output from the command (both stdout and stderr)
        self._output = ""


    @property
    def output(self) -> str:
        """
        Returns the output of the command.
        This string must include both stdout and stderr output.
        """
        return self._output


    @property
    def stream_config(self) -> StreamConfig:
        """
        Returns the stream configuration the logger wants.
        """
        return StreamConfig.SPLIT_STREAMS


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
        # This should never be None since the logger requests the streams to be
        #   split
        assert stderr is not None

        # Record stdout and stderr output into the output string
        pos = stdout.tell()
        stdout_contents = stdout.read()
        stdout.seek(pos)

        pos = stderr.tell()
        stderr_contents = stderr.read()
        stderr.seek(pos)

        self._output = stdout_contents + stderr_contents

        # Invoke each stream-specific logger
        self._stdout_logger.log(stdout, StringIO())
        self._stderr_logger.log(stderr, StringIO())


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
        self._stdout_logger.log_results(result, scanner_output)
        self._stderr_logger.log_results(result, scanner_output)
