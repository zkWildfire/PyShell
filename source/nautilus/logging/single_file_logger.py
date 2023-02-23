from nautilus.core.command import ICommand
from nautilus.core.command_result import CommandResult
from nautilus.logging.logger import ILogger
from pathlib import Path

class SingleFileLogger(ILogger):
    """
    Logs all commands' output to a single file.
    """
    def __init__(self, file_path: str):
        """
        Creates a new SingleFileLogger.
        @param file_path Path to the file to write logs to. Can be a relative or
          absolute path. If the path is a relative path, it will be interpreted
          relative to the directory that the Nautilus script is run from.
        """
        self._file_path = Path(file_path).absolute().resolve()

        # Clear the log file of any previous contents
        with open(self.file_path, "w") as _:
            pass


    @property
    def file_path(self) -> Path:
        """
        Path to the file to write logs to. Will always be an absolute path.
        """
        return self._file_path


    def log(self, command: ICommand, result: CommandResult) -> None:
        """
        Writes the result of a command to a log file.
        @param command Command that was run.
        @param result The result of the command.
        """
        with open(self.file_path, "a") as file:
            file.write(result.all_output)
