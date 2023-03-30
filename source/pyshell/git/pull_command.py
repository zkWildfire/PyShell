from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.external_command import ExternalCommand
from typing import Optional

class PullCommand(ExternalCommand):
    """
    Defines a command that runs `git pull`.
    @ingroup commands
    @ingroup git
    """
    def __init__(self,
        remote: Optional[str] = None,
        branch: Optional[str] = None,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param remote The remote to pull from.
        @param branch The branch to pull from the remote.
        @param cmd_flags The flags to set for the command.
        """
        args = ["pull"]
        if remote:
            args.append(remote)
        if branch:
            args.append(branch)

        super().__init__(
            "git",
            args,
            cmd_flags=cmd_flags
        )
