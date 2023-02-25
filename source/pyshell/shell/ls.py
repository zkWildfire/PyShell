from pathlib import Path
from pyshell.core.command import ICommand
from pyshell.core.command_result import CommandResult
from pyshell.core.pyshell import PyShell
from typing import Optional

class LsCommand(ICommand):
    """
    Defines a command that runs `ls`.
    """
    def __init__(self, target_path: str | Path | None = None):
        """
        Initializes the command.
        @param target_path The path to list the contents of.
        """
        super().__init__("ls", target_path)


    def __call__(self, pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs the command on the specified backend.
        @param pyshell PyShell instance to execute the command via.
        """
        pyshell = self._resolve_pyshell_instance(pyshell)
        return pyshell.run(self.full_command)
