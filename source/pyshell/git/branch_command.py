from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.external_command import ExternalCommand
from typing import List, Optional

class BranchCommand(ExternalCommand):
    """
    Defines a command that runs `git branch`.
    @ingroup commands
    @ingroup git
    """
    def __init__(self,
        branch: Optional[str],
        create_branch: bool = False,
        porcelain: bool = False,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param branch The branch to pass to the command.
        @param create_branch Whether to create the branch if it doesn't exist.
        @param porcelain Whether to use the porcelain format.
        @param cmd_flags The flags to set for the command.
        """
        # Determine what arguments should be passed to the command
        args: List[str] = ["branch"]
        if create_branch:
            args.append("-c")
        if porcelain:
            args.append("--porcelain")
        if branch:
            args.append(branch)

        super().__init__(
            "git",
            args,
            cmd_flags=cmd_flags
        )
