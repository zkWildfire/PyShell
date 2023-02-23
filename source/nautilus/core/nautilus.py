from __future__ import annotations
from nautilus.backends.backend import IBackend
from nautilus.core.command_result import CommandResult
from nautilus.error.error_handler import IErrorHandler
from nautilus.logging.logger import ILogger
from typing import Optional, Sequence

class Nautilus:
    """
    Contains all components required to execute Nautilus commands.
    """
    # Nautilus instance targeted when no instance is specified.
    _active_instance: Optional[Nautilus] = None


    def __init__(self,
        backend: IBackend,
        logger: ILogger,
        error_handler: IErrorHandler,
        set_as_active_instance: bool = True):
        """
        Initializes the Nautilus script.
        @param backend The backend to use to execute commands.
        @param error_handler The error handler to use to handle failed commands.
        @param set_as_active_instance Whether to set this instance as the
          currently active Nautilus instance.
        """
        self._backend = backend
        self._logger = logger
        self._error_handler = error_handler

        if set_as_active_instance:
            Nautilus._active_instance = self


    @staticmethod
    def active_instance() -> Optional[Nautilus]:
        """
        The currently active Nautilus instance.
        """
        return Nautilus._active_instance


    @staticmethod
    def get_required_active_instance() -> Nautilus:
        """
        Gets the currently active Nautilus instance.
        @throws ValueError If no Nautilus instance is currently active.
        """
        if not Nautilus._active_instance:
            raise ValueError("No active Nautilus instance.")
        return Nautilus._active_instance


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
        Sets this instance as the currently active Nautilus instance.
        Nautilus commands that do not have a Nautilus command explicitly
          specified as a target will use the currently active Nautilus instance.
        """
        Nautilus._active_instance = self
