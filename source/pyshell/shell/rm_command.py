from pathlib import Path
from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.external_command import ExternalCommand
from typing import List

class RmCommand(ExternalCommand):
    """
    Defines a command that runs `rm`.
    @ingroup commands
    @ingroup shell
    """
    def __init__(self,
        path: str | Path,
        force: bool = False,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param path Path to remove. Can be a relative or absolute path. If the
          path is relative, it will be resolved relative to the script's current
          working directory.
        @param force If True, the command will be run with the `-f` flag.
        @param cmd_flags The flags to set for the command.
        """
        # Determine what flags should be passed to the command
        flags: List[str] = []
        if force:
            flags.append("-f")

        if Path(path).is_dir():
            flags.append("-r")

        # TODO: Make this cross platform
        super().__init__("rm", flags + [path], cmd_flags=cmd_flags)
