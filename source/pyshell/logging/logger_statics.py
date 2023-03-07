from pathlib import Path
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.command_result import CommandResult
from pyshell.logging.logger_options import LoggerOptions
from typing import Any, List, Callable

class LoggerStatics:
    """
    Defines various static methods for logging.
    """
    @staticmethod
    def write_command_header(
        metadata: CommandMetadata,
        cwd: Path,
        write: Callable[[str], Any],
        options: LoggerOptions = LoggerOptions()) -> None:
        """
        Writes a command header to the callback.
        @param metadata The metadata of the command.
        @param cwd The current working directory of the command.
        @param write The callback to write the header to. Should not insert a
          newline after each call.
        @param options Options that control how the header is written.
        """
        # Determine what information should be printed within the banner
        lines: List[str] = []
        if options.print_cmd:
            lines.append(f"[PyShell] Running command: {metadata.full_command}")
        if options.print_cwd:
            lines.append(f"[PyShell] cwd: {cwd}")

        # If no values should be written, skip writing the command header
        if not lines:
            return

        # Print the banner
        write(options.cmd_header_banner + "\n")
        for line in lines:
            write(f"{options.cmd_header_banner_prefix}{line}\n")
        write(options.cmd_header_banner + "\n")

        if options.add_newline_after_header:
            write("\n")


    @staticmethod
    def write_command_footer(
        result: CommandResult,
        write: Callable[[str], Any],
        options: LoggerOptions = LoggerOptions()) -> None:
        """
        Writes a command footer to the callback.
        @param result The result of the command.
        @param write The callback to write the footer to.
        @param options Options that control how the footer is written.
        """
        # Determine what information should be printed within the banner
        lines: List[str] = []
        if options.print_cmd:
            lines.append(f"[PyShell] Executed command: {result.full_command}")
        if options.print_backend:
            lines.append(f"[PyShell] Backend: {result.backend}")
        if options.print_cwd:
            lines.append(f"[PyShell] cwd: {result.cwd}")
        if options.print_exit_code:
            lines.append(f"[PyShell] Command exited with code {result.exit_code}.")
        if options.print_timestamps:
            lines.append(f"[PyShell] Start time: {result.start_time_local}")
        if options.print_timestamps:
            lines.append(f"[PyShell] End time: {result.end_time_local}")
        if options.print_duration:
            if result.duration_milliseconds < 1000:
                lines.append(
                    f"[PyShell] Duration: {round(result.duration_milliseconds, 3)} ms"
                )
            elif result.duration_seconds < 60:
                lines.append(
                    f"[PyShell] Duration: {round(result.duration_seconds, 3)} s"
                )
            else:
                lines.append(
                    f"[PyShell] Duration: {round(result.duration_minutes, 3)} min"
                )

        # If no values should be written, skip writing the command footer
        if not lines:
            return

        # Print the banner
        write(options.cmd_footer_banner + "\n")
        for line in lines:
            write(f"{options.cmd_footer_banner_prefix}{line}\n")
        write(options.cmd_footer_banner + "\n")

        if options.add_newline_after_footer:
            write("\n")
