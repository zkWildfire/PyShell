from pathlib import Path
from pyshell.core.command_metadata import CommandMetadata
from pyshell.logging.console_command_logger import ConsoleCommandLogger
from pyshell.logging.file_command_logger import FileCommandLogger
from pyshell.logging.command_logger import ICommandLogger
from pyshell.logging.logger import ILogger
from pyshell.logging.tee_command_logger import TeeCommandLogger
from pyshell.logging.stream_config import StreamConfig

class SingleFileLogger(ILogger):
    """
    Logs all commands' output to a single file.
    @ingroup logging
    """
    def __init__(self,
        file_path: str | Path,
        print_cmd_header: bool = False,
        print_cmd_footer: bool = False):
        """
        Creates a new SingleFileLogger.
        @param file_path Path to the file to write logs to. Can be a relative or
          absolute path. If the path is a relative path, it will be interpreted
          relative to the directory that the PyShell script is run from.
        @param print_cmd_header Whether to print command info for each command
          that is run before the command's output.
        @param print_cmd_footer Whether to print command info for each command
            that is run after the command's output.
        """
        self._file_path = Path(file_path).absolute().resolve()
        self._print_cmd_header = print_cmd_header
        self._print_cmd_footer = print_cmd_footer

        # Make sure the log file's directory exists
        self._file_path.parent.mkdir(parents=True, exist_ok=True)

        # Clear the log file of any previous contents
        with open(self.file_path, "w") as _:
            pass


    @property
    def file_path(self) -> Path:
        """
        Path to the file to write logs to. Will always be an absolute path.
        """
        return self._file_path


    def construct_logger(self,
        metadata: CommandMetadata,
        cwd: Path) -> ICommandLogger:
        """
        Constructs a new command logger.
        @param metadata The metadata of the command that will the command logger
          will be used for.
        @param cwd The current working directory of the command that will the
          command logger will be used for.
        @return A new command logger instance.
        """
        console_logger = ConsoleCommandLogger(
            metadata,
            cwd,
            print_header=self._print_cmd_header,
            print_footer=self._print_cmd_footer
        )
        file_logger = FileCommandLogger(
            metadata,
            cwd,
            self.file_path,
            append=True,
            add_header=self._print_cmd_header,
            add_footer=self._print_cmd_footer
        )
        return TeeCommandLogger(
            StreamConfig.MERGE_STREAMS,
            [
                console_logger,
                file_logger
            ]
        )
