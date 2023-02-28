from pathlib import Path
from pyshell.backends.backend import IBackend
from pyshell.core.command_metadata import CommandMetadata
from pyshell.core.command_result import CommandResult
import subprocess
from typing import IO

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
            cwd=str(cwd),
            universal_newlines=True
        )

        # Process all output from the process
        assert process.stdout
        while process.poll() is None:
            new_output = NativeBackend._get_output(process.stdout)
            if new_output:
                output += new_output
                print(new_output, end="")

        # Process any remaining output from the process
        while True:
            new_output = NativeBackend._get_output(process.stdout)
            if new_output:
                # These lines are timing dependent; don't track them for coverage
                output += new_output # pragma: no cover
                print(new_output, end="") # pragma: no cover
            else:
                break

        # Add a final newline if the output doesn't end with one
        if not output.endswith("\n"):
            output += "\n"

        return CommandResult(
            command=metadata.command,
            args=metadata.args,
            cwd=str(cwd),
            output=output,
            exit_code=process.returncode,
            skipped=False
        )


    @staticmethod
    def _get_output(stream: IO[str]) -> str:
        """
        Gets the current output from the specified stream.
        This method will only return full lines of output. If the stream has
          partial output, this method will return None.
        @param stream The stream to get output from.
        @return The current output from the stream.
        """
        return stream.read()
