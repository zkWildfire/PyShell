from pathlib import Path
from pyshell.core.command import ICommand
from pyshell.core.command_result import CommandResult
from pyshell.core.pyshell import PyShell
from typing import List, Optional

class CpCommand(ICommand):
    """
    Defines a command that runs `cp`.
    """
    def __init__(self,
        src: str | Path,
        dest: str | Path):
        """
        Initializes the command.
        @param src File or directory to copy. Can be a relative or absolute
          path. If the path is relative, it will be resolved relative to the
          script's current working directory.
        @param dest Destination to copy the file or directory to. Can be a
          relative or absolute path. If the path is relative, it will be
          resolved relative to the script's current working directory.
        """
        # Validate input
        src = Path(src)
        dest = Path(dest)
        if not src.exists():
            raise ValueError(f"Source path {src} does not exist.")
        if not dest.exists():
            raise ValueError(f"Destination path {dest} does not exist.")

        # Determine what flags should be passed to the command
        flags: List[str] = []

        if src.is_dir():
            flags.append("-r")

        # TODO: Make this cross platform
        super().__init__("cp", flags + [src, dest])


    def __call__(self, pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs the command on the specified backend.
        @param pyshell PyShell instance to execute the command via.
        """
        pyshell = self._resolve_pyshell_instance(pyshell)
        return pyshell.run(self.full_command)
