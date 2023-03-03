from io import StringIO
from pathlib import Path
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.command_result import CommandResult
from pyshell.logging.console_command_logger import ConsoleCommandLogger
from pyshell.logging.split_command_logger import SplitCommandLogger
from pyshell.logging.stream_config import StreamConfig

class TestSplitCommandLogger:
    # Metadata instance passed to the logger used by tests
    metadata = CommandMetadata("command", ["arg1", "arg2"])

    def test_check_stream_config(self):
        console_logger = ConsoleCommandLogger(self.metadata, Path.cwd())
        logger = SplitCommandLogger(console_logger, console_logger)

        # For the split logger to work correctly, its stream config must be
        #   SPLIT_STREAMS.
        assert logger.stream_config == StreamConfig.SPLIT_STREAMS


    def test_log_stdout_output(self):
        msg = "foo bar"

        stdout_output = ""
        def on_stdout(x: str) -> None:
            nonlocal stdout_output
            stdout_output += x

        stderr_output = ""
        def on_stderr(x: str) -> None:
            nonlocal stderr_output
            stderr_output += x

        stdout_logger = ConsoleCommandLogger(
            self.metadata,
            Path.cwd(),
            on_stdout
        )
        stderr_logger = ConsoleCommandLogger(
            self.metadata,
            Path.cwd(),
            on_stderr
        )
        logger = SplitCommandLogger(stdout_logger, stderr_logger)
        stream = StringIO(msg)
        logger.log(stream, StringIO())
        assert msg in stdout_output
        assert not stderr_output
        assert msg in logger.output


    def test_log_stderr_output(self):
        msg = "foo bar"

        stdout_output = ""
        def on_stdout(x: str) -> None:
            nonlocal stdout_output
            stdout_output += x

        stderr_output = ""
        def on_stderr(x: str) -> None:
            nonlocal stderr_output
            stderr_output += x

        stdout_logger = ConsoleCommandLogger(
            self.metadata,
            Path.cwd(),
            on_stdout
        )
        stderr_logger = ConsoleCommandLogger(
            self.metadata,
            Path.cwd(),
            on_stderr
        )
        logger = SplitCommandLogger(stdout_logger, stderr_logger)
        stream = StringIO(msg)
        logger.log(StringIO(), stream)
        assert msg in stderr_output
        assert not stdout_output
        assert msg in logger.output


    def test_log_command_result(self):
        # Set up the logger
        stdout_output = ""
        def on_stdout(x: str) -> None:
            nonlocal stdout_output
            stdout_output += x

        stderr_output = ""
        def on_stderr(x: str) -> None:
            nonlocal stderr_output
            stderr_output += x

        stdout_logger = ConsoleCommandLogger(
            self.metadata,
            Path.cwd(),
            on_stdout,
            True,
            True
        )
        stderr_logger = ConsoleCommandLogger(
            self.metadata,
            Path.cwd(),
            on_stderr,
            True,
            True
        )

        logger = SplitCommandLogger(stdout_logger, stderr_logger)

        # Run the test
        result = CommandResult("foo", ["bar"], "/tmp", "", 0, False)
        logger.log_results(result, [])

        # Both loggers should have been invoked
        # This is necessary since loggers may run cleanup code in their
        #   `log_results()` method, so the split logger must invoke both
        #   loggers' `log_results()` method.
        assert stdout_output
        assert stderr_output
