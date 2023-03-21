from datetime import datetime
from dateutil import tz
from pyshell.commands.command_result import CommandResult
from typing import Optional, Sequence

class SyncCommandResult(CommandResult):
    """
    Stores the result of a command executed synchronously.
    @ingroup commands
    """
    def __init__(self,
        command: str,
        args: Sequence[str],
        cwd: str,
        output: str,
        exit_code: int,
        skipped: bool,
        start_time: datetime,
        end_time: datetime,
        backend: Optional[str] = None):
        """
        Initializes the object.
        @param command Name of the command/executable that was run.
        @param args Arguments passed to the command.
        @param cwd Working directory used for the command.
        @param output Merged output from stdout and stderr.
        @param exit_code Exit code from the command. If the command was skipped,
          this may be any value.
        @param skipped Whether the command was skipped.
        @param start_time The time the command started. Should be in UTC time.
        @param end_time The time the command ended. Should be in UTC time.
        @param backend Information about the backend that executed the command.
          The exact format of this string is backend-specific.
        """
        super().__init__()

        self._command = command
        self._args = args
        self._cwd = cwd
        self._output = output
        self._exit_code = exit_code
        self._skipped = skipped
        self._start_time = start_time
        self._end_time = end_time
        self._backend = backend


    @property
    def command(self) -> str:
        """
        Name of the command/executable that was run.
        """
        return self._command


    @property
    def args(self) -> Sequence[str]:
        """
        Arguments passed to the command.
        """
        return self._args


    @property
    def cwd(self) -> str:
        """
        Working directory used for the command.
        """
        return self._cwd


    @property
    def output(self) -> str:
        """
        Merged output from stdout and stderr.
        """
        return self._output


    @property
    def exit_code(self) -> int:
        """
        Exit code from the command.
        @throws RuntimeError If the command was skipped.
        """
        if self.skipped:
            raise RuntimeError("Cannot get exit code for skipped command.")
        return self._exit_code


    @property
    def success(self) -> bool:
        """
        Whether the command was successful.
        """
        return not self.skipped and self.exit_code == 0


    @property
    def error(self) -> bool:
        """
        Whether the command was not successful.
        """
        return not self.skipped and not self.success


    @property
    def skipped(self) -> bool:
        """
        Whether the command was skipped.
        """
        return self._skipped


    @property
    def full_command(self) -> str:
        """
        The full command that was run, including the command and all arguments.
        """
        return " ".join([self.command] + list(self.args))


    @property
    def start_time_utc(self) -> datetime:
        """
        The time the command started.
        """
        return self._start_time.astimezone(tz.tzutc())


    @property
    def start_time_local(self) -> datetime:
        """
        The time the command started, in local time.
        """
        return self.start_time_utc.astimezone(tz.tzlocal())


    @property
    def end_time_utc(self) -> datetime:
        """
        The time the command ended.
        """
        return self._end_time.astimezone(tz.tzutc())


    @property
    def end_time_local(self) -> datetime:
        """
        The time the command ended, in local time.
        """
        return self.end_time_utc.astimezone(tz.tzlocal())


    @property
    def duration_milliseconds(self) -> float:
        """
        The duration of the command, in milliseconds.
        """
        return self.duration_seconds * 1000


    @property
    def duration_seconds(self) -> float:
        """
        The duration of the command, in seconds.
        """
        return (self.end_time_utc - self.start_time_utc).total_seconds()


    @property
    def duration_minutes(self) -> float:
        """
        The duration of the command, in minutes.
        """
        return self.duration_seconds / 60


    @property
    def backend(self) -> Optional[str]:
        """
        Information about the backend that executed the command.
        The exact format of this string is backend-specific.
        """
        return self._backend


    def __bool__(self) -> bool:
        """
        Whether the command was successful.
        """
        return self.success
