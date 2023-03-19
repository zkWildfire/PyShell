from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.external_command import ExternalCommand
from typing import List

class StatusCommand(ExternalCommand):
    """
    Defines a command that runs `git branch`.
    @ingroup commands
    @ingroup git
    """
    def __init__(self,
        porcelain: bool = False,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param porcelain Whether to use the porcelain format.
        @param cmd_flags The flags to set for the command.
        """
        # Determine what arguments should be passed to the command
        args: List[str] = ["status"]
        if porcelain:
            args.append("--porcelain")

        super().__init__(
            "git",
            args,
            cmd_flags=cmd_flags
        )
