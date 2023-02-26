from pathlib import Path
from pyshell.backends.backend import IBackend
from pyshell.core.command_metadata import CommandMetadata
from pyshell.core.command_result import CommandResult

class DryRunBackend(IBackend):
    """
    Backend that prints commands without executing them.
    @ingroup backends
    """
    def run(self,
        metadata: CommandMetadata,
        cwd: Path) -> CommandResult:
        """
        Runs the specified command on the backend.
        @param command The command to run.
        @param cwd The working directory to use for the command. Will always be
          an absolute path.
        @return The output of the command.
        """
        print(metadata.full_command)

        return CommandResult(
            metadata=metadata,
            cwd=str(cwd),
            output="",
            exit_code=0,
            skipped=False
        )
