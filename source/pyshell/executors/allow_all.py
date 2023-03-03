from pyshell.commands.command_metadata import CommandMetadata
from pyshell.executors.executor import IExecutor

class AllowAll(IExecutor):
    """
    Executor that allows all commands except inactive commands to run.
    @ingroup executors
    """
    def should_run(self, metadata: CommandMetadata) -> bool:
        """
        Determines whether a command should be run.
        @param metadata Metadata for the command about to be run.
        @returns True if the command should be allowed to run. False if the
          command should be skipped.
        """
        return not metadata.is_inactive
