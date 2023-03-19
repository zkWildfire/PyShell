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
        branch: Optional[str] = None,
        create_branch: bool = False,
        show_current: bool = False,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param branch The branch to pass to the command.
        @param create_branch Whether to create the branch if it doesn't exist.
        @param show_current Whether to show the current branch.
        @param cmd_flags The flags to set for the command.
        """
        # Determine what arguments should be passed to the command
        args: List[str] = ["branch"]
        if create_branch:
            args.append("-c")
        if show_current:
            args.append("--show-current")
        if branch:
            args.append(branch)

        super().__init__(
            "git",
            args,
            cmd_flags=cmd_flags
        )
