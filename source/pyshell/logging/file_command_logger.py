from pathlib import Path
from pyshell.core.command_flags import CommandFlags
from pyshell.core.command_metadata import CommandMetadata
from pyshell.core.command_result import CommandResult
from pyshell.logging.command_logger import ICommandLogger
from pyshell.logging.stream_config import StreamConfig
from pyshell.scanners.entry import Entry
from typing import List, IO, Optional


class FileCommandLogger(ICommandLogger):
    """
    Logger that writes command output to a file.
    """
    def __init__(self,
        metadata: CommandMetadata,
        cwd: Path,
        file_path: str | Path,
        add_header: bool,
        add_footer: bool) -> None:
        """
        Initializes the logger.
        @param metadata The metadata of the command being run.
        @param file_path The path to the file to write to. If the file already
          exists, its contents will be overwritten.
        @param cwd The current working directory of the command.
        @param add_header Whether to add a command header to the file.
        @param add_footer Whether to add a command footer to the file.
        """
        self._metadata = metadata
        self._cwd = cwd
        self._file_path = Path(file_path)
        self._add_header = add_header
        self._add_footer = add_footer

        # Make sure the path to the file exists
        if not self._file_path.parent.exists():
            self._file_path.parent.mkdir(parents=True)

        # Clear the file of any previous contents
        self._file = open(self._file_path, "w")

        # Check whether the command's output shouldn't be logged
        self._skip_logging = False
        self._skip_logging &= metadata.flags & CommandFlags.QUIET
        self._skip_logging &= metadata.flags & CommandFlags.NO_FILE

        if not self._skip_logging and add_header:
            self._write_header()


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

        self._file.write(stdout.read())


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
        if self._skip_logging:
            return

        # Write any scanner entries to the file
        if scanner_output:
            self._file.write(f"[PyShell] Scanner output:\n")
        for entry in scanner_output:
            self._file.write("\n")
            self._file.write(entry.scanner_output)

        # Add the footer if requested
        if self._add_footer:
            self._file.write("\n")
            self._write_footer(result)
        self._file.write("\n")

        self._file.close()


    def _write_header(self) -> None:
        """
        Writes a header to the file.
        @pre The logger's output file is open.
        """
        self._file.write(
            f"[PyShell] Running command: {self._metadata.full_command}\n"
        )
        self._file.write(f"[PyShell] cwd: {self._cwd}\n")
        self._file.write(f"[PyShell] Command output:\n")


    def _write_footer(self, result: CommandResult) -> None:
        """
        Writes a footer to the file.
        @pre The logger's output file is open.
        """
        self._file.write(
            f"[PyShell] Executed command: {result.full_command}\n"
        )
        self._file.write(f"[PyShell] cwd: {result.cwd}\n")
        self._file.write(
            f"[PyShell] Command exited with code {result.exit_code}.\n"
        )
