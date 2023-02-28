from pathlib import Path
from pyshell.core.command_flags import CommandFlags
from pyshell.core.external_command import ExternalCommand

class LsCommand(ExternalCommand):
    """
    Defines a command that runs `ls`.
    @ingroup commands
    @ingroup shell
    """
    def __init__(self,
        target_path: str | Path | None = None,
        cmd_flags: CommandFlags = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param target_path The path to list the contents of.
        @param cmd_flags The flags to set for the command.
        """
        super().__init__(
            "ls",
            target_path,
            cmd_flags=cmd_flags
        )
