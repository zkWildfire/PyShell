from datetime import datetime
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.command_result import CommandResult
from pyshell.commands.sync_command_result import SyncCommandResult
from pyshell.logging.command_logger import ICommandLogger
import subprocess
from typing import Optional, Sequence

class AsyncCommandResult(CommandResult):
    """
    Stores the result of a command executed asynchronously.
    @ingroup commands
    """
    def __init__(self,
        proc: subprocess.Popen[str],
        logger: ICommandLogger,
        metadata: CommandMetadata,
        cwd: str,
        start_time: datetime,
        backend: str):
        """
        Initializes the result instance.
        @param proc The process that was executed.
        @param logger The logger to use to log the command.
        @param metadata Metadata for the command that was executed.
        @param cwd The working directory used for the command.
        @param start_time The time the command started. Should be in UTC time.
        @param backend Information about the backend that executed the command.
        """
        self._proc = proc
        self._logger = logger
        self._metadata = metadata
        self._cwd = cwd
        self._start_time = start_time
        self._backend = backend

        ## Command result instance set once the process exits.
        self._result: Optional[SyncCommandResult] = None


    @property
    def command(self) -> str:
        """
        Name of the command/executable that was run.
        """
        self.wait()
        assert self._result is not None
        return self._result.command


    @property
    def args(self) -> Sequence[str]:
        """
        Arguments passed to the command.
        """
        self.wait()
        assert self._result is not None
        return self._result.args


    @property
    def cwd(self) -> str:
        """
        Working directory used for the command.
        """
        self.wait()
        assert self._result is not None
        return self._result.cwd


    @property
    def output(self) -> str:
        """
        Merged output from stdout and stderr.
        """
        self.wait()
        assert self._result is not None
        return self._result.output


    @property
    def exit_code(self) -> int:
        """
        Exit code from the command.
        @throws RuntimeError If the command was skipped.
        """
        self.wait()
        assert self._result is not None
        return self._result.exit_code


    @property
    def success(self) -> bool:
        """
        Whether the command was successful.
        """
        self.wait()
        assert self._result is not None
        return self._result.success


    @property
    def error(self) -> bool:
        """
        Whether the command was not successful.
        """
        self.wait()
        assert self._result is not None
        return self._result.error


    @property
    def skipped(self) -> bool:
        """
        Whether the command was skipped.
        """
        self.wait()
        assert self._result is not None
        return self._result.skipped


    @property
    def full_command(self) -> str:
        """
        The full command that was run, including the command and all arguments.
        """
        self.wait()
        assert self._result is not None
        return self._result.full_command


    @property
    def start_time_utc(self) -> datetime:
        """
        The time the command started.
        """
        self.wait()
        assert self._result is not None
        return self._result.start_time_utc


    @property
    def start_time_local(self) -> datetime:
        """
        The time the command started, in local time.
        """
        self.wait()
        assert self._result is not None
        return self._result.start_time_local


    @property
    def end_time_utc(self) -> datetime:
        """
        The time the command ended.
        """
        self.wait()
        assert self._result is not None
        return self._result.end_time_utc


    @property
    def end_time_local(self) -> datetime:
        """
        The time the command ended, in local time.
        """
        self.wait()
        assert self._result is not None
        return self._result.end_time_local


    @property
    def duration_milliseconds(self) -> float:
        """
        The duration of the command, in milliseconds.
        """
        self.wait()
        assert self._result is not None
        return self._result.duration_milliseconds


    @property
    def duration_seconds(self) -> float:
        """
        The duration of the command, in seconds.
        """
        self.wait()
        assert self._result is not None
        return self._result.duration_seconds


    @property
    def duration_minutes(self) -> float:
        """
        The duration of the command, in minutes.
        """
        self.wait()
        assert self._result is not None
        return self._result.duration_minutes


    @property
    def backend(self) -> Optional[str]:
        """
        Information about the backend that executed the command.
        The exact format of this string is backend-specific.
        """
        self.wait()
        assert self._result is not None
        return self._result.backend


    def wait(self) -> SyncCommandResult:
        """
        Blocks until the process has exited.
        If the process has already exited, returns immediately.
        @post self._result is not None.
        @returns The result of the command.
        """
        # If this method has already been called, return immediately
        if self._result is not None:
            return self._result

        # The process's stderr is allowed to be null since it could be
        #   redirected, but the process's stdout must always be valid
        assert self._proc.stdout

        # Wait for the process to exit
        while self._proc.poll() is None:
            self._logger.log(self._proc.stdout, self._proc.stderr)

        # Process any remaining output from the process
        self._logger.log(self._proc.stdout, self._proc.stderr)

        # Make sure the returned output always ends with a newline
        output = self._logger.output
        if not output.endswith("\n"):
            output += "\n"

        self._result = SyncCommandResult(
            command=self._metadata.command,
            args=self._metadata.args,
            cwd=self._cwd,
            output=output,
            exit_code=self._proc.returncode,
            skipped=False,
            start_time=self._start_time,
            end_time=datetime.utcnow(),
            backend=self._backend
        )
        return self._result
