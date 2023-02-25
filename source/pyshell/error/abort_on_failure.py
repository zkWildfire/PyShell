from pyshell.core.command_result import CommandResult
from pyshell.error.error_handler import IErrorHandler

class AbortOnFailure(IErrorHandler):
    """
    Error handler that stops a PyShell script if a command fails.
    """
    def handle(self, result: CommandResult) -> None:
        """
        Handles a command that returned a non-zero exit code.
        @param command Command that was run.
        @param result The result of the command.
        """
        if not result.success:
            raise RuntimeError(
                f"Command '{result.command}' failed with exit code " + \
                    f"{result.exit_code}."
            )
