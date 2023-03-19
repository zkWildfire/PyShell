from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.external_command import ExternalCommand

class PushCommand(ExternalCommand):
    """
    Defines a command that runs `git push`.
    @ingroup commands
    @ingroup git
    """
    def __init__(self,
        remote: str = "origin",
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param remote The remote to pull from.
        @param cmd_flags The flags to set for the command.
        """
        super().__init__(
            "git",
            ["push", remote],
            cmd_flags=cmd_flags
        )
