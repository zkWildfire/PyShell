from pathlib import Path
from pyshell.core.command import ICommand
from pyshell.core.command_result import CommandResult
from pyshell.core.pyshell import PyShell
from typing import List, Optional

class RmCommand(ICommand):
    """
    Defines a command that runs `rm`.
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


    def __call__(self, pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs the command on the specified backend.
        @param pyshell PyShell instance to execute the command via.
        """
        pyshell = self._resolve_pyshell_instance(pyshell)
        return pyshell.run(self.full_command)
