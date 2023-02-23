from nautilus.backends.backend import IBackend
from nautilus.core.command_result import CommandResult
import subprocess
from typing import Sequence

class BareMetalBackend(IBackend):
    """
    Backend that executes commands directly.
    """

    def run(self, command: Sequence[str]) -> CommandResult:
        """
        Runs the specified command on the backend.
        @param command The command to run.
        @return The output of the command.
        """
        # Strings that process output will be written to
        all_output = ""
        stdout = ""
        stderr = ""

        # Start the process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Process all output from the process
        while process.poll() is None:
            assert process.stdout
            assert process.stderr

            # Read stdout and stderr
            new_stdout = process.stdout.readline().decode("utf-8")
            new_stderr = process.stderr.readline().decode("utf-8")

            # Update all output variables
            all_output += stdout + stderr
            stdout += new_stdout
            stderr += new_stderr

            # Also print output from the process so it's displayed in real
            #   time on the console
            if new_stdout:
                print(new_stdout)
            if new_stderr:
                print(new_stderr)

        return CommandResult(
            command=" ".join(command),
            all_output="TODO",
            stdout="TODO",
            stderr="TODO",
            exit_code=process.returncode,
            success=process.returncode == 0
        )
