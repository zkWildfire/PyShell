from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.external_command import ExternalCommand
from typing import Optional

class PushCommand(ExternalCommand):
    """
    Defines a command that runs `git push`.
    @ingroup commands
    @ingroup git
    """
    def __init__(self,
        remote: Optional[str] = None,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param remote The remote to pull from.
        @param cmd_flags The flags to set for the command.
        """
        args = ["push"]
        if remote:
            args.append(remote)

        super().__init__(
            "git",
            args,
            cmd_flags=cmd_flags
        )
