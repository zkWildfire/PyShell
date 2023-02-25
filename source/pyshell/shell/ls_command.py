from pathlib import Path
from pyshell.core.external_command import ExternalCommand

class LsCommand(ExternalCommand):
    """
    Defines a command that runs `ls`.
    @ingroup commands
    @ingroup shell
    """
    def __init__(self, target_path: str | Path | None = None):
        """
        Initializes the command.
        @param target_path The path to list the contents of.
        """
        super().__init__("ls", target_path)
