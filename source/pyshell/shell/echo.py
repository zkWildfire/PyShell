from pyshell.core.command import ICommand
from pyshell.core.command_result import CommandResult
from pyshell.core.pyshell import PyShell
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


    def __call__(self, pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs the command on the specified backend.
        @param pyshell PyShell instance to execute the command via.
        """
        pyshell = self._resolve_pyshell_instance(pyshell)
        return pyshell.run(self.full_command)
