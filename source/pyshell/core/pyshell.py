from __future__ import annotations
import os
from pathlib import Path
from pyshell.backends.backend import IBackend
from pyshell.core.command_result import CommandResult
from pyshell.core.pyshell_options import PyShellOptions
from pyshell.error.error_handler import IErrorHandler
from pyshell.logging.logger import ILogger
from typing import Optional, Sequence

class PyShell:
    """
    Contains all components required to execute PyShell commands.
    """
    # PyShell instance targeted when no instance is specified.
    _active_instance: Optional[PyShell] = None


    def __init__(self,
        backend: IBackend,
        logger: ILogger,
        error_handler: IErrorHandler,
        options: PyShellOptions,
        cwd: str | Path | None = None,
        set_as_active_instance: bool = True):
        """
        Initializes the PyShell script.
        @param backend The backend to use to execute commands.
        @param logger The logger to use to log commands.
        @param error_handler The error handler to use to handle failed commands.
        @param options Options for this PyShell instance.
        @param cwd The current working directory for this PyShell instance. If
          not specified, the current working directory of the script will be
          used.
        @param set_as_active_instance Whether to set this instance as the
          currently active PyShell instance.
        """
        self._backend = backend
        self._logger = logger
        self._options = options
        self._error_handler = error_handler

        # Initialize the cwd
        if cwd:
            self._cwd = Path(cwd).resolve()
        else:
            self._cwd = Path(os.getcwd()).resolve()

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
        command: Sequence[str],
        cwd: str | Path | None) -> CommandResult:
        """
        Runs the specified command on the backend.
        @param command The command to run.
        @param cwd The current working directory to use when running the
          command. If not specified, the current working directory of this
          PyShell instance will be used.
        @return The output of the command.
        """
        # Determine what cwd to use for the command
        if isinstance(cwd, str):
            cwd = Path(cwd)
        elif not cwd:
            cwd = self._cwd

        if not cwd.is_absolute():
            cwd = self._cwd.joinpath(cwd)

        # Run the command
        result = self._backend.run(command, cwd)

        # Handle post-command tasks
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
