from pathlib import Path
from pyshell.core.external_command import IExternalCommand

class LsCommand(IExternalCommand):
    """
    Defines a command that runs `ls`.
    @ingroup commands
    """
    def __init__(self, target_path: str | Path | None = None):
        """
        Initializes the command.
        @param target_path The path to list the contents of.
        """
        super().__init__("ls", target_path)
