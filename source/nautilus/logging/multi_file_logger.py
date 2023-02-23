from nautilus.core.command import ICommand
from nautilus.core.command_result import CommandResult
from nautilus.logging.logger import ILogger
import os
from pathlib import Path

class MultiFileLogger(ILogger):
    """
    Logs each commands' output to a separate file.
    """
    def __init__(self, output_dir: str):
        """
        Creates a new MultiFileLogger.
        @param output_dir Directory to write log files to. Can be a relative or
          absolute path. If the path is a relative path, it will be interpreted
          relative to the directory that the Nautilus script is run from.
        """
        self._output_dir = Path(output_dir).absolute().resolve()

        # Keep track of the number of commands that have been processed. This
        #   value is prepended to the name of each log file to ensure that log
        #   files are shown chronologically when sorted by name.
        self._cmd_count = 0

        # Clear out any existing log files
        for file in os.listdir(self._output_dir):
            os.remove(os.path.join(self._output_dir, file))


    @property
    def output_dir(self) -> Path:
        """
        Directory that log files are written to. Will always be an absolute path.
        """
        return self._output_dir


    def log(self, command: ICommand, result: CommandResult) -> None:
        """
        Writes the result of a command to a log file.
        @param command Command that was run.
        @param result The result of the command.
        """
        # Get the name of the file that the command's output will be written to
        self._cmd_count += 1
        file_path = self.output_dir / \
            f"{self._cmd_count}-{command.command_name}.log"

        # Write the command's output to the file
        with open(file_path, "w") as file:
            file.write(result.all_output)
