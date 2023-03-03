from pathlib import Path
from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.external_command import ExternalCommand
from typing import List, Optional

class CpCommand(ExternalCommand):
    """
    Defines a command that runs `cp`.
    @ingroup commands
    @ingroup shell
    """
    def __init__(self,
        src: str | Path,
        dest: str | Path,
        cmd_flags: int = CommandFlags.STANDARD):
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
        self._src = Path(src)
        self._dest = Path(dest)

        # Determine what flags should be passed to the command
        flags: List[str] = []

        if self._src.is_dir():
            flags.append("-r")

        # TODO: Make this cross platform
        super().__init__(
            "cp",
            flags + [src, dest],
            cmd_flags=cmd_flags
        )


    def _validate_args(self) -> Optional[str]:
        """
        Validates the arguments for the command.
        This method should be overridden by subclasses to validate the arguments
          for the command. If the arguments are valid, this method should
          return None. If the arguments are invalid, this method should return
          a string describing the error.
        @returns None if the arguments are valid, or a string describing the
          error if the arguments are invalid.
        """
        if not self._src.exists():
            return f"Source path '{self._src}' does not exist."
        return None
