import os
from pathlib import Path
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.logging.console_command_logger import ConsoleCommandLogger
from pyshell.logging.file_command_logger import FileCommandLogger
from pyshell.logging.command_logger import ICommandLogger
from pyshell.logging.logger import ILogger
from pyshell.logging.tee_command_logger import TeeCommandLogger
from pyshell.logging.stream_config import StreamConfig

class MultiFileLogger(ILogger):
    """
    Logs each commands' output to a separate file.
    @ingroup logging
    """
    # Name of the logs directory used by default.
    DEFAULT_LOGS_DIR = ".logs"

    def __init__(self,
        output_dir: str | Path = DEFAULT_LOGS_DIR,
        print_cmd_header: bool = False,
        print_cmd_footer: bool = False,
        clean_logs_dir: bool = True):
        """
        Creates a new MultiFileLogger.
        @param output_dir Directory to write log files to. Can be a relative or
          absolute path. If the path is a relative path, it will be interpreted
          relative to the directory that the PyShell script is run from.
        @param print_cmd_header Whether to print command info for each command
          that is run before the command's output.
        @param print_cmd_footer Whether to print command info for each command
            that is run after the command's output.
        @param clean_logs_dir Whether to delete any existing log files in the
          output directory before logging begins.
        @throws ValueError If 'output_dir' is a file.
        """
        self._print_cmd_header = print_cmd_header
        self._print_cmd_footer = print_cmd_footer
        self._output_dir = Path(output_dir).resolve()
        if self._output_dir.is_file():
            raise ValueError(f"'{self._output_dir}' is a file.")

        self._generate_output_dir()

        # Keep track of the number of commands that have been processed. This
        #   value is prepended to the name of each log file to ensure that log
        #   files are shown chronologically when sorted by name.
        self._cmd_count = 0

        # Clear out any existing log files
        if clean_logs_dir:
            for file in os.listdir(self._output_dir):
                os.remove(os.path.join(self._output_dir, file))


    @property
    def output_dir(self) -> Path:
        """
        Directory that log files are written to. Will always be an absolute path.
        """
        return self._output_dir


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
        # Get the name of the command to write to the log name
        cmd_name = metadata.command.split(os.path.sep)[-1]

        # Get the file name to use for the current command
        self._cmd_count += 1
        file_path = self.output_dir / f"{self._cmd_count}-{cmd_name}.log"

        # Create the logger
        console_logger = ConsoleCommandLogger(
            metadata,
            cwd,
            print_header=self._print_cmd_header,
            print_footer=self._print_cmd_footer
        )
        file_logger = FileCommandLogger(
            metadata,
            cwd,
            file_path,
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


    def _generate_output_dir(self):
        """
        Generates the directory to write log files to.
        The directory will be created if it does not already exist. If the
          directory already exists, this will be a no-op.
        """
        # Create the logs directory if it does not exist
        if not os.path.exists(self._output_dir):
            os.makedirs(self._output_dir)
