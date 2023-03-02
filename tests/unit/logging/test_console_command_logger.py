from io import StringIO
from pyshell.core.command_metadata import CommandMetadata
from pyshell.core.command_result import CommandResult
from pyshell.logging.console_command_logger import ConsoleCommandLogger
from pyshell.logging.stream_config import StreamConfig

class TestConsoleCommandLogger:
    # Metadata instance passed to the logger used by tests
    metadata = CommandMetadata("command", ["arg1", "arg2"])


    def test_check_stream_config(self):
        """
        Verify that the logger wants to merge stdout and stderr.
        A test case exists to verify this because the rest of the logger is
          built around this assumption. If the stream config is changed, the
          logger implementation will need to be heavily modified (and this test
          case removed).
        """
        logger = ConsoleCommandLogger(self.metadata)
        assert logger.stream_config == StreamConfig.MERGE_STREAMS


    def test_stdout_output_printed(self):
        msg = "foo bar"
        output = ""
        def on_print(x: str) -> None:
            nonlocal output
            output += x

        logger = ConsoleCommandLogger(self.metadata, on_print)
        stream = StringIO(msg)
        logger.log(stream, None)
        assert logger.output == msg


    def test_stderr_ignored(self):
        msg = "foo bar"
        output = ""
        def on_print(x: str) -> None:
            nonlocal output
            output += x

        logger = ConsoleCommandLogger(self.metadata, on_print)
        stdout = StringIO()
        stderr = StringIO(msg)
        logger.log(stdout, stderr)
        assert not logger.output


    def test_log_command_result(self):
        # Set up the logger
        output = ""
        def on_print(x: str) -> None:
            nonlocal output
            output += x
        logger = ConsoleCommandLogger(self.metadata, on_print)

        # Run the test
        cmd_name = "command"
        args = ["arg1", "arg2"]
        exit_code = 0
        result = CommandResult(cmd_name, args, "", "", exit_code, False)
        logger.log_results(result, [])

        # Validate results
        assert cmd_name in output
        for arg in args:
            assert arg in output
        assert str(exit_code) in output
