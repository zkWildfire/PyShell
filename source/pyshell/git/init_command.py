from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.external_command import ExternalCommand
from typing import Optional

class InitCommand(ExternalCommand):
    """
    Defines a command that runs `git init`.
    @ingroup commands
    @ingroup git
    """
    def __init__(self,
        branch_name: Optional[str],
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param branch_name The name to use for the initial branch. If not
          specified, uses the current git version's default branch name.
        @param cmd_flags The flags to set for the command.
        """
        args = ["init"]
        if branch_name:
            args.append("-b")
            args.append(branch_name)

        super().__init__(
            "git",
            args,
            cmd_flags=cmd_flags
        )
