from nautilus.core.command_result import CommandResult
from nautilus.logging.logger import ILogger
from pathlib import Path

class SingleFileLogger(ILogger):
    """
    Logs all commands' output to a single file.
    """
    def __init__(self, file_path: str, print_cmds: bool = False):
        """
        Creates a new SingleFileLogger.
        @param file_path Path to the file to write logs to. Can be a relative or
          absolute path. If the path is a relative path, it will be interpreted
          relative to the directory that the Nautilus script is run from.
        @param print_cmds Whether to print the command string for each command
            that is run before the command's output.
        """
        self._file_path = Path(file_path).absolute().resolve()
        self._print_cmds = print_cmds

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
        @param command Command that was run.
        @param result The result of the command.
        """
        with open(self.file_path, "a") as file:
            if self._print_cmds:
                file.write(f"[Nautilus] Running command: {result.full_command}\n")
            file.write(result.output)

            # Add a newline between different commands' output
            file.write("\n")
