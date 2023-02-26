from pyshell.core.command_metadata import CommandMetadata
from pyshell.core.command_result import CommandResult
from pyshell.error.error_handler import IErrorHandler
import sys

class KeepGoing(IErrorHandler):
    """
    Error handler that prints an error message but does not halt execution.
    @ingroup error
    """
    def should_run(self, metadata: CommandMetadata) -> bool:
        """
        Whether the command should be allowed to run.
        @param metadata Metadata for the command about to be run.
        @returns True if the command should be allowed to run.
        """
        # Always allow commands to be run regardless of failure
        return True


    def handle(self, result: CommandResult) -> None:
        """
        Handles a command that returned a non-zero exit code.
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
