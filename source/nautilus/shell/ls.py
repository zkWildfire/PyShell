from nautilus.core.command import ICommand
from nautilus.core.command_result import CommandResult
from nautilus.core.nautilus import Nautilus
from typing import Optional

class LsCommand(ICommand):
    """
    Defines a command that runs `ls`.
    """
    def __init__(self, target_path: Optional[str] = None):
        """
        Initializes the command.
        @param target_path The path to list the contents of.
        """
        super().__init__("ls", [target_path] if target_path is not None else [])


    def __call__(self, nautilus: Optional[Nautilus] = None) -> CommandResult:
        """
        Runs the command on the specified backend.
        @param nautilus Nautilus instance to execute the command via.
        """
        nautilus = self._resolve_nautilus_instance(nautilus)
        return nautilus.run(self.full_command)
