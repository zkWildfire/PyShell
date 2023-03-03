from io import StringIO
from pathlib import Path
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.command_result import CommandResult
from pyshell.logging.console_command_logger import ConsoleCommandLogger
from pyshell.logging.split_command_logger import SplitCommandLogger
from pyshell.logging.stream_config import StreamConfig
from pyshell.logging.tee_command_logger import TeeCommandLogger
import pytest

class TestTeeCommandLogger:
    # Metadata instance passed to the logger used by tests
    metadata = CommandMetadata("command", ["arg1", "arg2"])

    def test_check_stream_config(self):
        """
        Verifies that the tee logger's stream config property matches the value
          passed to its ctor.
        """
        console_logger = ConsoleCommandLogger(self.metadata, Path.cwd())
        logger = TeeCommandLogger(console_logger.stream_config, console_logger)
        assert logger.stream_config == console_logger.stream_config


    def test_ctor_throws_if_loggers_not_compatible_with_stream_config(self):
        """
        Verifies that the tee logger's ctor throws an exception if the loggers
          passed to it are not compatible with the stream config passed to it.
        """
        console_logger = ConsoleCommandLogger(self.metadata, Path.cwd())
        with pytest.raises(RuntimeError):
            target_stream_config = StreamConfig.SPLIT_STREAMS
            # This is a required prerequisite for the test to be valid, but is
            #   not technically part of the test.
            assert console_logger.stream_config != target_stream_config

            TeeCommandLogger(target_stream_config, console_logger)


    def test_log_to_stdout(self):
        msg = "foo bar"
        output = ""
        def on_print(x: str) -> None:
            nonlocal output
            output += x

        console_logger = ConsoleCommandLogger(
            self.metadata,
            Path.cwd(),
            on_print
        )
        logger = TeeCommandLogger(StreamConfig.MERGE_STREAMS, console_logger)
        stream = StringIO(msg)
        logger.log(stream, None)
        assert output == msg


    def test_log_to_stderr(self):
        # Set up the loggers
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
            False,
            False
        )
        stderr_logger = ConsoleCommandLogger(
            self.metadata,
            Path.cwd(),
            on_stderr,
            False,
            False
        )
        split_logger = SplitCommandLogger(stdout_logger, stderr_logger)
        tee_logger = TeeCommandLogger(StreamConfig.SPLIT_STREAMS, split_logger)

        # Run the test
        msg = "foo bar"
        stream = StringIO(msg)
        tee_logger.log(StringIO(), stream)

        # Verify the results
        assert not stdout_output
        assert msg in stderr_output
        assert msg in tee_logger.output


    def test_log_command_result(self):
        # Set up the logger
        output = ""
        def on_print(x: str) -> None:
            nonlocal output
            output += x
        console_logger = ConsoleCommandLogger(
            self.metadata,
            Path.cwd(),
            on_print,
            True,
            True
        )
        logger = TeeCommandLogger(StreamConfig.MERGE_STREAMS, console_logger)

        # Run the test
        result = CommandResult("foo", ["bar"], "/tmp", "", 0, False)
        logger.log_results(result, [])
        assert output


    def test_ctor_throws_if_logger_list_is_empty(self):
        with pytest.raises(RuntimeError):
            TeeCommandLogger(StreamConfig.MERGE_STREAMS, [])
