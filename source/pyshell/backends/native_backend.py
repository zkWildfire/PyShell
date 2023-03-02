from pathlib import Path
from pyshell.backends.backend import IBackend
from pyshell.core.command_metadata import CommandMetadata
from pyshell.core.command_result import CommandResult
from pyshell.logging.command_logger import ICommandLogger
from pyshell.logging.stream_config import StreamConfig
import subprocess
from typing import IO

class NativeBackend(IBackend):
    """
    Backend that executes commands directly.
    @ingroup backends
    """

    def run(self,
        metadata: CommandMetadata,
        cwd: Path,
        logger: ICommandLogger) -> CommandResult:
        """
        Runs the specified command on the backend.
        @param metadata Metadata for the command to run.
        @param cwd The working directory to use for the command. Will always be
          an absolute path.
        @param logger The logger to use for the command. The backend will invoke
          `logger.log()` but will not invoke `logger.log_results()`.
        @return The output of the command.
        """
        # Determine how stderr should be handled
        if logger.stream_config == StreamConfig.SPLIT_STREAMS:
            process_stderr = subprocess.PIPE
        elif logger.stream_config == StreamConfig.MERGE_STREAMS:
            process_stderr = subprocess.STDOUT
        else:
            assert False

        # Start the process
        process = subprocess.Popen(
            [metadata.command] + list(metadata.args),
            stdout=subprocess.PIPE,
            stderr=process_stderr,
            cwd=str(cwd),
            universal_newlines=True
        )

        # The process's stderr is allowed to be null since it could be
        #   redirected, but the process's stdout must always be valid
        assert process.stdout

        # Process all output from the process
        while process.poll() is None:
            logger.log(process.stdout, process.stderr)

        # Process any remaining output from the process
        logger.log(process.stdout, process.stderr)

        # Make sure the returned output always ends with a newline
        output = logger.output
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
