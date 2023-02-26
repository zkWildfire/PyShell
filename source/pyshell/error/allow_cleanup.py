from pyshell.core.command_metadata import CommandMetadata
from pyshell.core.command_result import CommandResult
from pyshell.error.error_handler import IErrorHandler
import sys

class AllowCleanup(IErrorHandler):
    """
    Error handler that prevents non-cleanup commands from running after an error.
    @ingroup error
    """
    def __init__(self):
        """
        Initializes the object.
        """
        # Whether an error has occurred
        self._has_failed = False


    def handle(self, result: CommandResult) -> None:
        """
        Handles a command that returned a non-zero exit code.
        @param result The result of the command.
        """
        print(
            f"Command '{result.command}' failed with exit code " + \
                f"{result.exit_code}.\n",
            file=sys.stderr
        )
        print(
            f"Note: Full command was '{result.full_command}'.",
            file=sys.stderr
        )
        self._has_failed = True


    def should_run(self, metadata: CommandMetadata) -> bool:
        """
        Whether the command should be allowed to run.
        @param metadata Metadata for the command about to be run.
        @returns True if the command should be allowed to run.
        """
        # If a failure has occurred, only allow cleanup commands to run
        if self._has_failed:
            return metadata.is_cleanup
        else:
            return True
