from pathlib import Path
from pyshell.core.command_result import CommandResult
from pyshell.logging.logger import ILogger

class SingleFileLogger(ILogger):
    """
    Logs all commands' output to a single file.
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


    def log(self, result: CommandResult) -> None:
        """
        Writes the result of a command to a log file.
        @param result The result of the command.
        """
        with open(self.file_path, "a") as file:
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

            # Add a newline between different commands' output
            file.write("\n")
