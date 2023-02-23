from nautilus.core.command import ICommand
from nautilus.core.command_result import CommandResult
from nautilus.core.nautilus import Nautilus
from typing import Optional

class EchoCommand(ICommand):
    """
    Defines a command that runs `echo`.
    """
    def __init__(self, message: Optional[str] = None):
        """
        Initializes the command.
        @param message The message to write to stdout.
        """
        super().__init__("echo", [message] if message is not None else [])


    def __call__(self, nautilus: Optional[Nautilus] = None) -> CommandResult:
        """
        Runs the command on the specified backend.
        @param nautilus Nautilus instance to execute the command via.
        """
        nautilus = self._resolve_nautilus_instance(nautilus)
        return nautilus.run(self.full_command)
