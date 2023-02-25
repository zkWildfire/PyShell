from abc import ABC, abstractmethod
from pathlib import Path
from pyshell.core.command_result import CommandResult
from pyshell.core.pyshell import PyShell
from typing import Optional, Sequence

class ICommand(ABC):
    """
    Represents a command that may be executed by a backend.
    @ingroup commands
    """
    @property
    @abstractmethod
    def command_name(self) -> str:
        """
        The name of the command being run.
        This contains the name of the executable/command being run but does not
          include any of the arguments.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def args(self) -> Sequence[str]:
        """
        The arguments passed to the command.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def full_command(self) -> Sequence[str]:
        """
        The full command being run, including the command name and all arguments.
        """
        raise NotImplementedError()


    @abstractmethod
    def __call__(self,
        pyshell: Optional[PyShell] = None,
        cwd: str | Path | None = None) -> CommandResult:
        """
        Runs the command on the specified backend.
        @param pyshell PyShell instance to execute the command via.
        @param cwd The current working directory to use for the command. If this
          is not provided, the pyshell instance's cwd will be used.
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
