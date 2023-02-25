from abc import ABC, abstractmethod
from pathlib import Path
from pyshell.core.command_result import CommandResult
from pyshell.core.pyshell import PyShell
from typing import Optional, Sequence

class ICommand(ABC):
    """
    Represents a command that may be executed by a backend.
    """
    def __init__(self,
        name: str | Path,
        args: str | Path | Sequence[str | Path] | None = None):
        """
        Initializes the command.
        @param name The name of the command being run. This should be the name
          of the executable/command being run but should not include any of
          the arguments.
        @param args The argument(s) to pass to the command.
        """
        self._name = str(name)
        if isinstance(args, str) or isinstance(args, Path):
            args = [args]
        elif not args:
            args = []
        self._args = [str(a) for a in args]


    @property
    def command_name(self) -> str:
        """
        The name of the command being run.
        This contains the name of the executable/command being run but does not
          include any of the arguments.
        """
        return self._name


    @property
    def args(self) -> Sequence[str]:
        """
        The arguments passed to the command.
        """
        return self._args


    @property
    def full_command(self) -> Sequence[str]:
        """
        The full command being run, including the command name and all arguments.
        """
        return [self.command_name] + self._args


    @abstractmethod
    def __call__(self, pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs the command on the specified backend.
        @param pyshell PyShell instance to execute the command via.
        """
        raise NotImplementedError()


    def _resolve_pyshell_instance(self,
        pyshell: Optional[PyShell] = None) -> PyShell:
        """
        Helper method used to get the PyShell instance to use for the command.
        @param pyshell The PyShell instance passed to the command.
        @return The PyShell instance to use for the command. This will be the
          instance passed to the command if it is not None, otherwise it will
          be the active instance.
        """
        if pyshell:
            return pyshell
        else:
            return PyShell.get_required_active_instance()
