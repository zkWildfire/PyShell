from pyshell.core.command_flags import CommandFlags
from pyshell.core.command_metadata import CommandMetadata
from pyshell.core.command_result import CommandResult
from pyshell.logging.command_logger import ICommandLogger
from pyshell.logging.stream_config import StreamConfig
from pyshell.scanners.entry import Entry
from typing import Any, Callable, List, IO, Optional

class ConsoleCommandLogger(ICommandLogger):
    """
    Logger that writes command output to the console.
    @ingroup logging
    """
    def __init__(self,
        metadata: CommandMetadata,
        print: Callable[[str], Any] = lambda x: print(x)) \
            -> None:
        """
        Initializes the logger.
        @param metadata The metadata of the command being run.
        @param print The print function to use for logging. The functor will be
          passed the string to output to stdout. A newline character should not
          be appended by the functor. Any return value will be ignored.
        """
        self._metadata = metadata
        self._print = print

        # Stores all output from the command
        self._output = ""

        # Check whether the command's output shouldn't be logged
        self._skip_logging = False
        self._skip_logging |= metadata.flags & CommandFlags.QUIET
        self._skip_logging |= metadata.flags & CommandFlags.NO_CONSOLE


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
        return StreamConfig.MERGE_STREAMS


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
        # Check if any output exists to be logged
        cmd_output = stdout.read()
        if not cmd_output:
            return

        # Always update `self._output`
        self._output += cmd_output

        # Print the output if logging is enabled
        if self._skip_logging:
            return
        self._print(cmd_output)


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
        self._print(f"Command exited with code {result.exit_code}.\n")
        self._print(f"Note: Command was '{result.full_command}'.\n\n")
