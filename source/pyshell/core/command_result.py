from typing import NamedTuple, Sequence

class CommandResult(NamedTuple):
    """
    Stores the result of a command execution.
    """
    # Name of the command/executable that was run
    command: str

    # Arguments passed to the command
    args: Sequence[str]

    # Full command, including the command name and all arguments
    full_command: str

    # Merged output from stdout and stderr
    output: str

    # Exit code from the command
    exit_code: int

    # Whether the command was successful
    success: bool
