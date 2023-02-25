from pathlib import Path
from pyshell.backends.backend import IBackend
from pyshell.core.command_result import CommandResult
import subprocess
from typing import Sequence

class NativeBackend(IBackend):
    """
    Backend that executes commands directly.
    @ingroup backends
    """

    def run(self,
        command: Sequence[str],
        cwd: Path) -> CommandResult:
        """
        Runs the specified command on the backend.
        @param command The command to run.
        @param cwd The working directory to use for the command. Will always be
          an absolute path.
        @return The output of the command.
        """
        output = ""

        # Start the process
        process = subprocess.Popen(
            command,
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

        # Add a final newline if the output doesn't end with one
        if output and not output.endswith("\n"):
            output += "\n"

        return CommandResult(
            command=command[0],
            args=command[1:],
            cwd=str(cwd),
            output=output,
            exit_code=process.returncode
        )
