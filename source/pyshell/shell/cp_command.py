from pathlib import Path
from pyshell.core.command_flags import CommandFlags
from pyshell.core.external_command import ExternalCommand
from typing import List

class CpCommand(ExternalCommand):
    """
    Defines a command that runs `cp`.
    @ingroup commands
    @ingroup shell
    """
    def __init__(self,
        src: str | Path,
        dest: str | Path,
        cmd_flags: CommandFlags = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param src File or directory to copy. Can be a relative or absolute
          path. If the path is relative, it will be resolved relative to the
          script's current working directory.
        @param dest Destination to copy the file or directory to. Can be a
          relative or absolute path. If the path is relative, it will be
          resolved relative to the script's current working directory.
        @param cmd_flags The flags to set for the command.
        @throws ValueError If the source path does not exist.
        """
        # Validate input
        src = Path(src)
        dest = Path(dest)
        if not src.exists():
            raise ValueError(f"Source path {src} does not exist.")

        # Determine what flags should be passed to the command
        flags: List[str] = []

        if src.is_dir():
            flags.append("-r")

        # TODO: Make this cross platform
        super().__init__(
            "cp",
            flags + [src, dest],
            cmd_flags=cmd_flags
        )
