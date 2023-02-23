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
        output = ""

        # Start the process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        # Process all output from the process
        while process.poll() is None:
            assert process.stdout
            new_output = process.stdout.readline().decode("utf-8").rstrip()
            if new_output:
                output += new_output
                print(new_output)

        # Add a final newline if the output doesn't end with one
        if output and not output.endswith("\n"):
            output += "\n"

        return CommandResult(
            command=command[0],
            args=command[1:],
            full_command=" ".join(command),
            output=output,
            exit_code=process.returncode,
            success=process.returncode == 0
        )
