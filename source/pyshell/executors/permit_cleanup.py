from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.command_result import CommandResult
from pyshell.core.pyshell_events import PyShellEvents
from pyshell.executors.executor import IExecutor


class PermitCleanup(IExecutor):
    """
    Executor that allows only cleanup commands to be run after a failure.
    @ingroup executors
    """
    def __init__(self):
        """
        Initializes the object.
        """
        # Whether a command has failed
        self._failed = False


    def initialize(self, events: PyShellEvents) -> None:
        """
        Initializes the executor.
        @param events `PyShellEvents` instance for the pyshell instance that
          the executor is being used with.
        """
        events.on_command_failed += self._on_failure


    def should_run(self, metadata: CommandMetadata) -> bool:
        """
        Determines whether a command should be run.
        @param metadata Metadata for the command about to be run.
        @returns True if the command should be allowed to run. False if the
          command should be skipped.
        """
        # Regardless of whether a command has failed, inactive commands should
        #   not be run
        if metadata.is_inactive:
            return False

        # If a command has failed, only allow cleanup commands to be executed
        if self._failed:
            return metadata.is_cleanup

        # If no command has failed yet, allow any command to be run
        return True


    def _on_failure(self, sender: PyShellEvents, result: CommandResult) -> None:
        """
        Callback bound to the on_command_failed event.
        @param sender Sender of the event.
        @param result Result of the command that failed.
        """
        self._failed = True
