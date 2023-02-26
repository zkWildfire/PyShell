from pathlib import Path
from pyshell.backends.backend import IBackend
from pyshell.core.command_metadata import CommandMetadata
from pyshell.core.command_result import CommandResult
import subprocess

class NativeBackend(IBackend):
    """
    Backend that executes commands directly.
    @ingroup backends
    """

    def run(self,
        metadata: CommandMetadata,
        cwd: Path) -> CommandResult:
        """
        Runs the specified command on the backend.
        @param metadata Metadata for the command to run.
        @param cwd The working directory to use for the command. Will always be
          an absolute path.
        @return The output of the command.
        """
        output = ""

        # Start the process
        process = subprocess.Popen(
            [metadata.command] + list(metadata.args),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=str(cwd)
        )

        # Process all output from the process
        while process.poll() is None:
            assert process.stdout
            new_output = process.stdout.readline().decode("utf-8").rstrip()
            if new_output:
                output += new_output + "\n"
                print(new_output)

        # Process any remaining output from the process
        assert process.stdout
        new_output = process.stdout.read().decode("utf-8").rstrip()
        if new_output:
            output += new_output + "\n"
            print(new_output)

        return CommandResult(
            metadata=metadata,
            cwd=str(cwd),
            output=output,
            exit_code=process.returncode,
            skipped=False
        )
