from __future__ import annotations
from pyshell.backends.backend import IBackend
from pyshell.core.command_result import CommandResult
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
        set_as_active_instance: bool = True):
        """
        Initializes the PyShell script.
        @param backend The backend to use to execute commands.
        @param error_handler The error handler to use to handle failed commands.
        @param set_as_active_instance Whether to set this instance as the
          currently active PyShell instance.
        """
        self._backend = backend
        self._logger = logger
        self._error_handler = error_handler

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


    def run(self, command: Sequence[str]) -> CommandResult:
        """
        Runs the specified command on the backend.
        @param command The command to run.
        @return The output of the command.
        """
        result = self._backend.run(command)
        self._logger.log(result)
        if not result.success:
            self._error_handler.handle(result)
        return result


    def set_as_active_instance(self) -> None:
        """
        Sets this instance as the currently active PyShell instance.
        PyShell commands that do not have a PyShell command explicitly
          specified as a target will use the currently active PyShell instance.
        """
        PyShell._active_instance = self
