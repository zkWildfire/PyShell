from pyshell.core.command_result import CommandResult
from pyshell.logging.logger import ILogger
import os
from pathlib import Path

class MultiFileLogger(ILogger):
    """
    Logs each commands' output to a separate file.
    """
    # Name of the logs directory used by default.
    DEFAULT_LOGS_DIR = ".logs"

    def __init__(self,
        output_dir: str | Path = DEFAULT_LOGS_DIR,
        print_cmd_header: bool = False,
        print_cmd_footer: bool = False,
        clean_logs_dir: bool = False):
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


    def log(self, result: CommandResult) -> None:
        """
        Writes the result of a command to a log file.
        @param result The result of the command.
        """
        # Make sure the output directory exists
        # This is necessary in case the directory is removed, e.g. because a
        #   script cleans the log directory by removing it.
        self._generate_output_dir()

        # Get the name of the command to write to the log name
        cmd_name = result.command.split(os.path.sep)[-1]

        # Get the name of the file that the command's output will be written to
        self._cmd_count += 1
        file_path = self.output_dir / f"{self._cmd_count}-{cmd_name}.log"

        # Write the command's output to the file
        with open(file_path, "w") as file:
            # Add the header
            if self._print_cmd_header:
                file.write(f"[PyShell] Running command: {result.full_command}\n")
                file.write(f"[PyShell] cwd: {result.cwd}\n")
                file.write(f"[PyShell] Command output:\n")
                file.write("\n")

            # Write the command's output
            file.write(result.output)

            # Add the footer
            if self._print_cmd_footer:
                file.write("\n")
                file.write(f"[PyShell] Executed command: {result.full_command}\n")
                file.write(f"[PyShell] cwd: {result.cwd}\n")
                file.write(f"[PyShell] Command exited with code {result.exit_code}.\n")

            # Add a final newline
            file.write("\n")


    def _generate_output_dir(self):
        """
        Generates the directory to write log files to.
        The directory will be created if it does not already exist. If the
          directory already exists, this will be a no-op.
        """
        # Create the logs directory if it does not exist
        if not os.path.exists(self._output_dir):
            os.makedirs(self._output_dir)
