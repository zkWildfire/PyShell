from nautilus.core.command import ICommand
from nautilus.core.command_result import CommandResult
from nautilus.error.error_handler import IErrorHandler

class AbortOnFailure(IErrorHandler):
    """
    Error handler that stops a Nautilus script if a command fails.
    """
    def handle(self, command: ICommand, result: CommandResult) -> None:
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
