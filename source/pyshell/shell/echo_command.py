from pyshell.core.external_command import ExternalCommand
from typing import Optional

class EchoCommand(ExternalCommand):
    """
    Defines a command that runs `echo`.
    @ingroup commands
    @ingroup shell
    """
    def __init__(self, message: Optional[str] = None):
        """
        Initializes the command.
        @param message The message to write to stdout.
        """
        super().__init__("echo", message)
