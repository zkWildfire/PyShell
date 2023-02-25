from pathlib import Path
from pyshell.core.external_command import IExternalCommand
from typing import List

class RmCommand(IExternalCommand):
    """
    Defines a command that runs `rm`.
    @ingroup commands
    @ingroup shell
    """
    def __init__(self, path: str | Path, force: bool = False):
        """
        Initializes the command.
        @param path Path to remove. Can be a relative or absolute path. If the
          path is relative, it will be resolved relative to the script's current
          working directory.
        @param force If True, the command will be run with the `-f` flag.
        """
        # Determine what flags should be passed to the command
        flags: List[str] = []
        if force:
            flags.append("-f")

        if Path(path).is_dir():
            flags.append("-r")

        # TODO: Make this cross platform
        super().__init__("rm", flags + [path])
