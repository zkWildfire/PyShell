from abc import ABC, abstractmethod
from nautilus.backends.backend import IBackend
from nautilus.core.command_result import CommandResult
from typing import Optional, Sequence

class ICommand(ABC):
    """
    Represents a command that may be executed by a backend.
    """
    def __init__(self,
        name: str,
        args: Optional[Sequence[str]] = None):
        """
        Initializes the command.
        @param name The name of the command being run. This should be the name
          of the executable/command being run but should not include any of
          the arguments.
        @param args The arguments to pass to the command.
        """
        self._name = name
        self._args = list(args) if args is not None else []


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
    def __call__(self, backend: Optional[IBackend] = None) -> CommandResult:
        """
        Runs the command on the specified backend.
        @param backend: The backend to run the command on. If not provided, runs
          on the currently active backend.
        """
        raise NotImplementedError()
