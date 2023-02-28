from pyshell.core.command_flags import CommandFlags
from pyshell.core.external_command import ExternalCommand
from typing import Optional

class EchoCommand(ExternalCommand):
    """
    Defines a command that runs `echo`.
    @ingroup commands
    @ingroup shell
    """
    def __init__(self,
        message: Optional[str] = None,
        cmd_flags: CommandFlags = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param message The message to write to stdout.
        @param cmd_flags The flags to set for the command.
        """
        super().__init__(
            "echo",
            message,
            cmd_flags=cmd_flags
        )
