from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.external_command import ExternalCommand

class InitCommand(ExternalCommand):
    """
    Defines a command that runs `git init`.
    @ingroup commands
    @ingroup git
    """
    def __init__(self,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param branch The branch to switch to.
        @param create_branch Whether to create the branch if it doesn't exist.
        @param cmd_flags The flags to set for the command.
        """
        super().__init__(
            "git",
            ["init"],
            cmd_flags=cmd_flags
        )
