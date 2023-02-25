from pyshell.core.command_result import CommandResult
from pyshell.error.error_handler import IErrorHandler
import sys

class KeepGoing(IErrorHandler):
    """
    Error handler that prints an error message but does not halt execution.
    """
    def handle(self, result: CommandResult) -> None:
        """
        Handles a command that returned a non-zero exit code.
        @param command Command that was run.
        @param result The result of the command.
        """
        print(
            f"Command '{result.command}' failed with exit code " + \
                f"{result.exit_code}.",
            file=sys.stderr
        )
        print(
            f"Note: Full command was '{result.full_command}'.",
            file=sys.stderr
        )
