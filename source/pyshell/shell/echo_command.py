from pyshell.core.external_command import IExternalCommand
from typing import Optional

class EchoCommand(IExternalCommand):
    """
    Defines a command that runs `echo`.
    @ingroup commands
    """
    def __init__(self, message: Optional[str] = None):
        """
        Initializes the command.
        @param message The message to write to stdout.
        """
        super().__init__("echo", message)
