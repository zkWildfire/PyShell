from pathlib import Path
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.command_result import CommandResult
from typing import Any, Callable

class LoggerStatics:
    """
    Defines various static methods for logging.
    """
    @staticmethod
    def write_command_header(
        metadata: CommandMetadata,
        cwd: Path,
        write: Callable[[str], Any]) -> None:
        """
        Writes a command header to the callback.
        @param metadata The metadata of the command.
        @param cwd The current working directory of the command.
        @param write The callback to write the header to. Should not insert a
          newline after each call.
        """
        write(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
        write(f"[PyShell] Running command: {metadata.full_command}\n")
        write(f"[PyShell] cwd: {cwd}\n")
        write(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")


    @staticmethod
    def write_command_footer(
        result: CommandResult,
        write: Callable[[str], Any]) -> None:
        """
        Writes a command footer to the callback.
        @param result The result of the command.
        @param write The callback to write the footer to.
        """
        write("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
        write(
            f"[PyShell] Executed command: {result.full_command}\n"
        )
        if result.backend:
            write(f"[PyShell] Backend: {result.backend}\n")
        write(f"[PyShell] cwd: {result.cwd}\n")
        write(
            f"[PyShell] Command exited with code {result.exit_code}.\n"
        )
        write(f"[PyShell] Start time: {result.start_time_local}\n")
        write(f"[PyShell] End time: {result.end_time_local}\n")
        if result.duration_milliseconds < 1000:
            write(
                f"[PyShell] Duration: {result.duration_milliseconds} ms\n"
            )
        elif result.duration_seconds < 60:
            write(
                f"[PyShell] Duration: {result.duration_seconds} s\n"
            )
        else:
            write(
                f"[PyShell] Duration: {result.duration_minutes} min\n"
            )
        write("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n")
