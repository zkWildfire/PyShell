from datetime import datetime
from pathlib import Path
from pyshell.backends.backend import IBackend
from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.command_result import CommandResult
from pyshell.commands.async_command_result import AsyncCommandResult
from pyshell.logging.command_logger import ICommandLogger
from pyshell.logging.stream_config import StreamConfig
import subprocess

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
        else: # logger.stream_config == StreamConfig.MERGE_STREAMS:
            process_stderr = subprocess.STDOUT

        # Start the process
        start_time = datetime.utcnow()
        process = subprocess.Popen(
            [metadata.command] + list(metadata.args),
            stdout=subprocess.PIPE,
            stderr=process_stderr,
            cwd=str(cwd),
            universal_newlines=True
        )

        # If the command's async flag is set, return immediately. Otherwise,
        #   wait for the process to finish and return the results.
        result = AsyncCommandResult(
            process,
            logger,
            metadata,
            str(cwd),
            start_time,
            "Host"
        )

        if metadata.flags & CommandFlags.ASYNC:
            return result
        else:
            return result.wait()
