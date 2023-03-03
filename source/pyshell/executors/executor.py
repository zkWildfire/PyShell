from abc import abstractmethod
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.core.pyshell_component import IPyShellComponent

class IExecutor(IPyShellComponent):
    """
    Base interface for command executors.
    Command executors are classes that handle whether a command should be run.
    @ingroup executors
    """
    @abstractmethod
    def should_run(self, metadata: CommandMetadata) -> bool:
        """
        Determines whether a command should be run.
        @param metadata Metadata for the command about to be run.
        @returns True if the command should be allowed to run. False if the
          command should be skipped.
        """
        raise NotImplementedError()
