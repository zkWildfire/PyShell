from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.external_command import ExternalCommand
from typing import List

class SwitchCommand(ExternalCommand):
    """
    Defines a command that runs `git switch`.
    @ingroup commands
    @ingroup git
    """
    def __init__(self,
        branch: str,
        create_branch: bool = False,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param branch The branch to switch to.
        @param create_branch Whether to attempt to create the branch. If this
          is set to true and the branch already exists, the command will fail.
        @param cmd_flags The flags to set for the command.
        """
        # Determine what arguments should be passed to the command
        args: List[str] = ["switch"]
        if create_branch:
            args.append("-c")
        args.append(branch)

        super().__init__(
            "git",
            args,
            cmd_flags=cmd_flags
        )
