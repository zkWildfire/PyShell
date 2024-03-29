from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Sequence

class CommandResult(ABC):
    """
    Stores the result of a command execution.
    @ingroup commands
    """
    def __init__(self):
        """
        Initializes the object.
        """
        super().__init__()


    @property
    @abstractmethod
    def command(self) -> str:
        """
        Name of the command/executable that was run.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def args(self) -> Sequence[str]:
        """
        Arguments passed to the command.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def cwd(self) -> str:
        """
        Working directory used for the command.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def output(self) -> str:
        """
        Merged output from stdout and stderr.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def exit_code(self) -> int:
        """
        Exit code from the command.
        @throws RuntimeError If the command was skipped.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def success(self) -> bool:
        """
        Whether the command was successful.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def error(self) -> bool:
        """
        Whether the command was not successful.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def skipped(self) -> bool:
        """
        Whether the command was skipped.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def full_command(self) -> str:
        """
        The full command that was run, including the command and all arguments.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def start_time_utc(self) -> datetime:
        """
        The time the command started.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def start_time_local(self) -> datetime:
        """
        The time the command started, in local time.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def end_time_utc(self) -> datetime:
        """
        The time the command ended.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def end_time_local(self) -> datetime:
        """
        The time the command ended, in local time.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def duration_milliseconds(self) -> float:
        """
        The duration of the command, in milliseconds.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def duration_seconds(self) -> float:
        """
        The duration of the command, in seconds.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def duration_minutes(self) -> float:
        """
        The duration of the command, in minutes.
        """
        raise NotImplementedError()


    @property
    @abstractmethod
    def backend(self) -> Optional[str]:
        """
        Information about the backend that executed the command.
        The exact format of this string is backend-specific.
        """
        raise NotImplementedError()


    def __bool__(self) -> bool:
        """
        Whether the command was successful.
        """
        return self.exit_code == 0
