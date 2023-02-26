from typing import Sequence

class CommandResult:
    """
    Stores the result of a command execution.
    """
    def __init__(self,
        command: str,
        args: Sequence[str],
        cwd: str,
        output: str,
        exit_code: int):
        """
        Initializes the object.
        @param command Name of the command/executable that was run.
        @param args Arguments passed to the command.
        @param cwd Working directory used for the command.
        @param output Merged output from stdout and stderr.
        @param exit_code Exit code from the command.
        """
        self._command = command
        self._args = args
        self._cwd = cwd
        self._output = output
        self._exit_code = exit_code


    @property
    def command(self) -> str:
        """
        Name of the command/executable that was run.
        """
        return self._command


    @property
    def args(self) -> Sequence[str]:
        """
        Arguments passed to the command.
        """
        return self._args


    @property
    def cwd(self) -> str:
        """
        Working directory used for the command.
        """
        return self._cwd


    @property
    def output(self) -> str:
        """
        Merged output from stdout and stderr.
        """
        return self._output


    @property
    def exit_code(self) -> int:
        """
        Exit code from the command.
        """
        return self._exit_code


    @property
    def success(self) -> bool:
        """
        Whether the command was successful.
        """
        return self.exit_code == 0


    @property
    def error(self) -> bool:
        """
        Whether the command was not successful.
        """
        return not self.success


    @property
    def full_command(self) -> str:
        """
        The full command that was run, including the command and all arguments.
        """
        return " ".join([self.command] + list(self.args))
