from pyshell.core.command_result import CommandResult
from pyshell.logging.command_logger import ICommandLogger
from pyshell.logging.stream_config import StreamConfig
from pyshell.scanners.entry import Entry
from typing import List, IO, Optional

class TeeCommandLogger(ICommandLogger):
    """
    Command logger that pushes data to two or more loggers.
    """
    def __init__(self,
        stream_config: StreamConfig,
        loggers: List[ICommandLogger]) -> None:
        """
        Initializes the logger.
        @param stream_config The stream configuration to use. The caller is
          responsible for ensuring that all loggers in the `loggers` list
          support this stream configuration.
        @param loggers The loggers to push data to.
        """
        self._stream_config = stream_config
        self._loggers = loggers

        # Create stream objects for each logger
        # Each entry in this list will be a stdout stream and a stderr stream.
        self._streams = [(IO[str](), IO[str]()) for _ in loggers]


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
        # Push the data to each logger's stream
        for logger_stdout, logger_stderr in self._streams:
            logger_stdout.write(stdout.read())
            if stderr is not None:
                logger_stderr.write(stderr.read())

        # Invoke each logger
        for logger, (logger_stdout, logger_stderr) in \
            zip(self._loggers, self._streams):
            logger.log(logger_stdout, logger_stderr)


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
        for logger in self._loggers:
            logger.log_results(result, scanner_output)
