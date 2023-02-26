from pathlib import Path
from pyshell.backends.backend import IBackend
from pyshell.core.command_metadata import CommandMetadata
from pyshell.core.command_result import CommandResult
import subprocess
from typing import IO, Optional

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
        assert process.stdout
        while process.poll() is None:
            new_output = NativeBackend._get_output(process.stdout)
            if new_output:
                output += new_output + "\n"
                print(new_output)

        # Process any remaining output from the process
        new_output = NativeBackend._get_output(process.stdout)
        if new_output:
            output += new_output + "\n"
            print(new_output)

        return CommandResult(
            command=metadata.command,
            args=metadata.args,
            cwd=str(cwd),
            output=output,
            exit_code=process.returncode,
            skipped=False
        )


    @staticmethod
    def _get_output(stream: IO[bytes], max_lines: Optional[int] = None) \
        -> Optional[str]:
        """
        Gets the current output from the specified stream.
        This method will only return full lines of output. If the stream has
          partial output, this method will return None.
        @param stream The stream to get output from.
        @param max_lines The maximum number of lines to read from the stream.
          If this is not provided, all available lines will be read.
        @return The current output from the stream, or None if the stream has
          partial output.
        """
        output = ""
        line_count = 0

        while not max_lines or line_count < max_lines:
            line = stream.readline().decode("utf-8").rstrip()
            if not line:
                break
            output += line + "\n"
            line_count += 1

        return output if output else None
