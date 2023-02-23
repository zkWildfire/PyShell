from typing import NamedTuple

class CommandResult(NamedTuple):
    """
    Stores the result of a command execution.
    """
    # Command that was executed
    command: str

    # Merged output from stdout and stderr
    all_output: str

    # Output from the command stdout stream
    stdout: str

    # Output from the command's stderr stream
    stderr: str

    # Exit code from the command
    exit_code: int

    # Whether the command was successful
    success: bool
