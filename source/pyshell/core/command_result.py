from typing import NamedTuple, Sequence

class CommandResult(NamedTuple):
    """
    Stores the result of a command execution.
    """
    # Name of the command/executable that was run
    command: str

    # Arguments passed to the command
    args: Sequence[str]

    # Working directory used for the command
    # @invariant This will always be an absolute path.
    cwd: str

    # Merged output from stdout and stderr
    output: str

    # Exit code from the command
    exit_code: int


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
