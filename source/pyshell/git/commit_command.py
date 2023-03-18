from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.external_command import ExternalCommand
from typing import List

class CommitCommand(ExternalCommand):
    """
    Defines a command that runs `git commit`.
    @ingroup commands
    @ingroup git
    """
    def __init__(self,
        message: str,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param message The commit message.
        @param cmd_flags The flags to set for the command.
        """
        args: List[str] = ["add", "-m", message]
        super().__init__(
            "git",
            args,
            cmd_flags=cmd_flags
        )
