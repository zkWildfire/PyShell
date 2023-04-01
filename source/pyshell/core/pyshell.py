from __future__ import annotations
from datetime import datetime
from pathlib import Path
from pyshell.backends.backend import IBackend
from pyshell.backends.native_backend import NativeBackend
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.command_result import CommandResult
from pyshell.commands.sync_command_result import SyncCommandResult
from pyshell.core.pyshell_events import PyShellEvents
from pyshell.core.pyshell_options import PyShellOptions
from pyshell.error.abort_on_failure import AbortOnFailure
from pyshell.error.error_handler import IErrorHandler
from pyshell.events.event_handler import EventHandler
from pyshell.executors.executor import IExecutor
from pyshell.executors.allow_all import AllowAll
from pyshell.logging.console_logger import ConsoleLogger
from pyshell.logging.logger import ILogger
from typing import Callable, IO, Optional, Protocol

class PrintCallable(Protocol):
    """
    Helper type used to type hint the built-in `print()` function.
    """
    def __call__(self,
        *values: object,
        sep: str = " ",
        end: str = "\n",
        file: IO[str] | None = None,
        flush: bool = False) -> None:
        """
        Prints the specified values to the specified file.
        @param values The values to print.
        @param sep The separator to use between values.
        @param end The string to append to the end of the printed values.
        @param file The file to print to. If None, the default file is used.
        """
        pass


class PyShell:
    """
    Contains all components required to execute PyShell commands.
    """
    # PyShell instance targeted when no instance is specified.
    _active_instance: Optional[PyShell] = None


    def __init__(self,
        backend: IBackend = NativeBackend(),
        logger: ILogger = ConsoleLogger(),
        executor: IExecutor = AllowAll(),
        error_handler: IErrorHandler = AbortOnFailure(),
        options: PyShellOptions = PyShellOptions(),
        cwd: str | Path | None = None,
        set_as_active_instance: bool = True):
        """
        Initializes the PyShell script.
        @param backend The backend to use to execute commands.
        @param logger The logger to use to log commands.
        @param executor The executor to use to determine which commands to run.
        @param error_handler The error handler to use to handle failed commands.
        @param options Options for this PyShell instance.
        @param cwd The current working directory for this PyShell instance. If
          not specified, the current working directory of the script will be
          used.
        @param set_as_active_instance Whether to set this instance as the
          currently active PyShell instance.
        """
        self._backend = backend
        self._executor = executor
        self._logger = logger
        self._options = options
        self._error_handler = error_handler

        # Initialize the events
        # Note that the event handlers are stored in this class instead of the
        #   PyShellEvents class because the events will be broadcast to by this
        #   class, not the PyShellEvents class. However, the sender for each
        #   event will be the PyShellEvents instance to avoid circular
        #   references in class definitions.
        self._on_command_started: EventHandler[PyShellEvents, CommandMetadata] = \
            EventHandler()
        self._on_command_skipped: EventHandler[PyShellEvents, CommandMetadata] = \
            EventHandler()
        self._on_command_finished: EventHandler[PyShellEvents, CommandResult] = \
            EventHandler()
        self._on_command_failed: EventHandler[PyShellEvents, CommandResult] = \
            EventHandler()
        self._events = PyShellEvents(
            self._on_command_started,
            self._on_command_skipped,
            self._on_command_finished,
            self._on_command_failed
        )

        # Initialize each component
        self._backend.initialize(self._events)
        self._logger.initialize(self._events)
        self._executor.initialize(self._events)
        self._error_handler.initialize(self._events)

        # Initialize the cwd
        if cwd:
            self._cwd = Path(cwd).resolve()
        else:
            self._cwd = Path.cwd()

        # Set this instance as the active instance if requested
        if set_as_active_instance:
            PyShell._active_instance = self


    @staticmethod
    def active_instance() -> Optional[PyShell]:
        """
        The currently active PyShell instance.
        """
        return PyShell._active_instance


    @staticmethod
    def clear_active_instance() -> None:
        """
        Clears the currently active PyShell instance.
        """
        PyShell._active_instance = None


    @staticmethod
    def get_required_active_instance() -> PyShell:
        """
        Gets the currently active PyShell instance.
        @throws ValueError If no PyShell instance is currently active.
        """
        if not PyShell._active_instance:
            raise ValueError("No active PyShell instance.")
        return PyShell._active_instance


    @property
    def cwd(self) -> Path:
        """
        The current working directory for this PyShell instance.
        @invariant This will always be an absolute path.
        """
        return self._cwd


    @property
    def options(self) -> PyShellOptions:
        """
        Options for this PyShell instance.
        """
        return self._options


    def cd(self, value: str | Path) -> None:
        """
        Changes the current working directory for this PyShell instance.
        @param value The new current working directory. If this is a relative
          path, it will be resolved relative to the `cwd` value prior to this
          call.
        """
        value = Path(value)
        if not value.is_absolute():
            value = self._cwd.joinpath(value)
        self._cwd = value


    def print(self,
        *values: object,
        sep: str = " ",
        end: str = "\n",
        file: IO[str] | None = None,
        flush: bool = False,
        verbose: bool | int = 0,
        print_func: PrintCallable = print):
        """
        Prints a message to the console.
        This method takes into account the verbosity level that the PyShell
          instance was configured with and whether quiet mode is enabled.
        @param values The values to print.
        @param sep The separator to use between values.
        @param end The end of line character to use.
        @param file The file to print to. If not specified, the standard output
          stream will be used.
        @param flush Whether to flush the output stream after printing.
        @param verbose The minimum verbosity level required to print the
          message. If this is a boolean, it will be treated as 1 or 0 for True
          and False, respectively. The PyShell instance's verbosity level must
          be greater than or equal to this value for the message to be printed.
          Note that if quiet mode is enabled, the message will never be printed.
        @param print_func The function to use to print the message. This is
          primarily for testing purposes.
        """
        if isinstance(verbose, bool):
            verbose = int(verbose)

        # If the script is running in quiet mode, then don't print anything
        if self.options.quiet:
            return
        # Otherwise, print the message if the verbosity level is high enough
        elif self.options.verbose >= verbose:
            print_func(
                *values,
                sep=sep,
                end=end,
                file=file,
                flush=flush
            )


    def run(self,
        metadata: CommandMetadata,
        cwd: str | Path | None) -> CommandResult:
        """
        Runs the specified command on the backend.
        @param metadata The metadata for the command.
        @param cwd The current working directory to use when running the
          command. If not specified, the current working directory of this
          PyShell instance will be used.
        @return The output of the command.
        """
        # Determine what cwd to use for the command
        if not cwd:
            cwd = self._cwd
        cwd = Path(cwd)

        if not cwd.is_absolute():
            cwd = self._cwd.joinpath(cwd)
        cwd = cwd.resolve()

        # Determine whether to run the command
        if not self._executor.should_run(metadata):
            self._on_command_skipped.broadcast(self._events, metadata)
            return SyncCommandResult(
                metadata.command,
                metadata.args,
                str(cwd),
                "",
                0,
                True,
                datetime.now(),
                datetime.now()
            )

        # Run the command
        logger = self._logger.construct_logger(
            metadata,
            self._options.logger_options,
            cwd
        )
        self._on_command_started.broadcast(self._events, metadata)
        result = self._backend.run(metadata, cwd, logger)

        # Log the command output and result
        if metadata.scanner:
            scanner_results = metadata.scanner.scan_for_errors(result)
        else:
            scanner_results = []
        logger.log_results(result, scanner_results)

        # Handle post-command tasks
        if result.success:
            self._on_command_finished.broadcast(self._events, result)
        else:
            self._on_command_failed.broadcast(self._events, result)

        # This must be done after broadcasting to events since error handlers
        #   could cause the script to abort
        if not result.success:
            self._error_handler.handle(result)
        return result


    def is_active_instance(self) -> bool:
        """
        Whether this instance is the currently active PyShell instance.
        @returns True if this instance is the currently active PyShell instance.
        """
        return PyShell._active_instance is self


    def set_as_active_instance(self) -> None:
        """
        Sets this instance as the currently active PyShell instance.
        PyShell commands that do not have a PyShell command explicitly
          specified as a target will use the currently active PyShell instance.
        """
        PyShell._active_instance = self
