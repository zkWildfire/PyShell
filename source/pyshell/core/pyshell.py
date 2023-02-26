from __future__ import annotations
from pathlib import Path
from pyshell.backends.backend import IBackend
from pyshell.backends.native_backend import NativeBackend
from pyshell.core.command_metadata import CommandMetadata
from pyshell.core.command_result import CommandResult
from pyshell.core.pyshell_events import PyShellEvents
from pyshell.core.pyshell_options import PyShellOptions
from pyshell.error.abort_on_failure import AbortOnFailure
from pyshell.error.error_handler import IErrorHandler
from pyshell.events.event_handler import EventHandler
from pyshell.executors.executor import IExecutor
from pyshell.executors.allow_all import AllowAll
from pyshell.logging.logger import ILogger
from pyshell.logging.null_file_logger import NullFileLogger
from typing import Optional

class PyShell:
    """
    Contains all components required to execute PyShell commands.
    """
    # PyShell instance targeted when no instance is specified.
    _active_instance: Optional[PyShell] = None


    def __init__(self,
        backend: IBackend = NativeBackend(),
        logger: ILogger = NullFileLogger(),
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
            return CommandResult(metadata, str(cwd), "", 0, True)

        # Run the command
        self._on_command_started.broadcast(self._events, metadata)
        result = self._backend.run(metadata, cwd)

        # Handle post-command tasks
        if result.success:
            self._on_command_finished.broadcast(self._events, result)
        else:
            self._on_command_failed.broadcast(self._events, result)

        self._logger.log(result)
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
