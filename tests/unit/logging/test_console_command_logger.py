from io import StringIO
from pathlib import Path
from pyshell.core.command_flags import CommandFlags
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
        logger = ConsoleCommandLogger(self.metadata, Path.cwd())
        assert logger.stream_config == StreamConfig.MERGE_STREAMS


    def test_stdout_output_printed(self):
        msg = "foo bar"
        output = ""
        def on_print(x: str) -> None:
            nonlocal output
            output += x

        logger = ConsoleCommandLogger(self.metadata, Path.cwd(), on_print)
        stream = StringIO(msg)
        logger.log(stream, None)
        assert logger.output == msg


    def test_stderr_ignored(self):
        msg = "foo bar"
        output = ""
        def on_print(x: str) -> None:
            nonlocal output
            output += x

        logger = ConsoleCommandLogger(self.metadata, Path.cwd(), on_print)
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
        logger = ConsoleCommandLogger(
            self.metadata,
            Path.cwd(),
            on_print,
            True,
            True
        )

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


    def test_quiet_commands_are_not_logged(self):
        # Set up the metadata instance
        cmd_name = "command"
        args = ["arg1", "arg2"]
        metadata = CommandMetadata(cmd_name, args, CommandFlags.QUIET)

        # Set up the logger
        output = ""
        def on_print(x: str) -> None:
            nonlocal output
            output += x
        logger = ConsoleCommandLogger(metadata, Path.cwd(), on_print)

        # Run the test
        stdout = StringIO("foo bar baz")
        logger.log(stdout, None)

        # Validate results
        assert not output


    def test_no_console_commands_are_not_logged(self):
        # Set up the metadata instance
        cmd_name = "command"
        args = ["arg1", "arg2"]
        metadata = CommandMetadata(cmd_name, args, CommandFlags.NO_CONSOLE)

        # Set up the logger
        output = ""
        def on_print(x: str) -> None:
            nonlocal output
            output += x
        logger = ConsoleCommandLogger(metadata, Path.cwd(), on_print)

        # Run the test
        stdout = StringIO("foo bar baz")
        logger.log(stdout, None)

        # Validate results
        assert not output


    def test_no_file_commands_are_logged(self):
        # Set up the metadata instance
        cmd_name = "command"
        args = ["arg1", "arg2"]
        metadata = CommandMetadata(cmd_name, args, CommandFlags.NO_FILE)

        # Set up the logger
        output = ""
        def on_print(x: str) -> None:
            nonlocal output
            output += x
        logger = ConsoleCommandLogger(metadata, Path.cwd(), on_print)

        # Run the test
        msg = "foo bar baz"
        stdout = StringIO(msg)
        logger.log(stdout, None)

        # Validate results
        assert logger.output == msg


    def test_skip_results_output_if_logging_disabled(self):
        # Set up the metadata instance
        cmd_name = "command"
        args = ["arg1", "arg2"]
        metadata = CommandMetadata(cmd_name, args, CommandFlags.NO_CONSOLE)

        # Set up the logger
        output = ""
        def on_print(x: str) -> None:
            nonlocal output
            output += x
        logger = ConsoleCommandLogger(metadata, Path.cwd(), on_print)

        # Run the test
        exit_code = 0
        result = CommandResult(cmd_name, args, "", "", exit_code, False)
        logger.log_results(result, [])

        # Validate results
        assert not output
