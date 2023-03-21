from datetime import datetime
from io import StringIO
from pathlib import Path
from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.sync_command_result import SyncCommandResult
from pyshell.logging.file_command_logger import FileCommandLogger
from pyshell.logging.logger_options import LoggerOptions
from pyshell.logging.stream_config import StreamConfig
from pyshell.scanners.entry import Entry
from pyshell.scanners.severity import ESeverity
from typing import Any

class TestFileCommandLogger:
    # Metadata instance passed to the logger used by tests
    metadata = CommandMetadata("command", ["arg1", "arg2"])

    # Result instance used when closing the logger
    result = SyncCommandResult(
        "cmd",
        ["arg1", "arg2"],
        "/tmp",
        "",
        0,
        False,
        datetime.now(),
        datetime.now()
    )

    # Name of the file used by tests
    log_file_name = "output.log"

    def test_check_stream_config(self, tmp_path: Any):
        """
        Verify that the logger wants to merge stdout and stderr.
        A test case exists to verify this because the rest of the logger is
          built around this assumption. If the stream config is changed, the
          logger implementation will need to be heavily modified (and this test
          case removed).
        """
        logger = FileCommandLogger(
            self.metadata,
            LoggerOptions(),
            tmp_path,
            tmp_path / self.log_file_name,
            False,
            False,
            False
        )
        logger.log_results(self.result, [])
        assert logger.stream_config == StreamConfig.MERGE_STREAMS


    def test_stdout_output_printed(self, tmp_path: Any):
        # Set up the logger
        output_file = Path(tmp_path) / self.log_file_name
        msg = "foo bar"
        logger = FileCommandLogger(
            self.metadata,
            LoggerOptions(),
            tmp_path,
            output_file,
            False,
            False,
            False
        )

        # Run the test
        stream = StringIO(msg)
        logger.log(stream, None)
        logger.log_results(self.result, [])

        # Validate results
        assert msg in output_file.read_text()


    def test_stderr_ignored(self, tmp_path: Any):
        # Set up the logger
        output_file = Path(tmp_path) / self.log_file_name
        msg = "foo bar"
        logger = FileCommandLogger(
            self.metadata,
            LoggerOptions(),
            tmp_path,
            output_file,
            False,
            False,
            False
        )

        # Run the test
        stdout = StringIO()
        stderr = StringIO(msg)
        logger.log(stdout, stderr)
        logger.log_results(self.result, [])

        # Validate results
        assert not output_file.read_text().strip()


    def test_append_to_existing_file(self, tmp_path: Any):
        # Set up the logger
        output_file = Path(tmp_path) / self.log_file_name
        msg = "foo bar"
        output_file.write_text("bar foo")
        logger = FileCommandLogger(
            self.metadata,
            LoggerOptions(),
            tmp_path,
            output_file,
            False,
            False,
            False
        )

        # Run the test
        stdout = StringIO(msg)
        stderr = StringIO()
        logger.log(stdout, stderr)
        logger.log_results(self.result, [])

        # Validate results
        assert msg in output_file.read_text()


    def test_overwrite_existing_file(self, tmp_path: Any):
        # Set up the logger
        output_file = Path(tmp_path) / self.log_file_name
        msg = "foo bar"
        output_file.write_text("bar foo")
        logger = FileCommandLogger(
            self.metadata,
            LoggerOptions(),
            tmp_path,
            output_file,
            False,
            False,
            True
        )

        # Run the test
        stdout = StringIO(msg)
        stderr = StringIO()
        logger.log(stdout, stderr)
        logger.log_results(self.result, [])


        # Validate results
        assert msg in output_file.read_text()


    def test_log_command_result(self, tmp_path: Any):
        # Set up the logger
        output_file = Path(tmp_path) / self.log_file_name
        logger = FileCommandLogger(
            self.metadata,
            LoggerOptions(),
            tmp_path,
            output_file,
            False,
            False,
            True
        )

        # Run the test
        cmd_name = "command"
        args = ["arg1", "arg2"]
        result = SyncCommandResult(
            cmd_name,
            args,
            tmp_path,
            "",
            0,
            False,
            datetime.now(),
            datetime.now()
        )
        logger.log_results(result, [])

        # Validate results
        assert output_file.read_text()


    def test_log_scanner_entry(self, tmp_path: Any):
        # Set up the logger
        output_file = Path(tmp_path) / self.log_file_name
        logger = FileCommandLogger(
            self.metadata,
            LoggerOptions(),
            tmp_path,
            output_file,
            False,
            False,
            True
        )

        # Run the test
        scanner_msg = "bar"
        entry = Entry(ESeverity.ERROR, "foo", 0, 1, scanner_msg)
        result = SyncCommandResult(
            "cmd",
            ["arg1", "arg2"],
            tmp_path,
            "",
            0,
            False,
            datetime.now(),
            datetime.now()
        )
        logger.log_results(result, [entry])

        # Validate results
        assert scanner_msg in output_file.read_text()


    def test_write_header(self, tmp_path: Any):
        # Set up the logger
        output_file = Path(tmp_path) / self.log_file_name
        logger = FileCommandLogger(
            self.metadata,
            LoggerOptions(),
            tmp_path,
            output_file,
            False,
            True,
            False
        )

        # Close the file
        logger.log_results(self.result, [])

        # Validate results
        assert output_file.read_text().strip()


    def test_write_footer(self, tmp_path: Any):
        # Set up the logger
        output_file = Path(tmp_path) / self.log_file_name
        logger = FileCommandLogger(
            self.metadata,
            LoggerOptions(),
            tmp_path,
            output_file,
            False,
            False,
            True
        )

        # Close the file
        logger.log_results(self.result, [])

        # Validate results
        assert output_file.read_text().strip()


    def test_write_header_and_footer(self, tmp_path: Any):
        # Set up the logger
        output_file = Path(tmp_path) / self.log_file_name
        logger = FileCommandLogger(
            self.metadata,
            LoggerOptions(),
            tmp_path,
            output_file,
            False,
            True,
            True
        )

        # Close the file
        logger.log_results(self.result, [])

        # Validate results
        assert output_file.read_text().strip()


    def test_no_output_if_quiet(self, tmp_path: Any):
        # Set up the logger
        metadata = CommandMetadata("cmd", ["arg1", "arg2"], CommandFlags.QUIET)
        output_file = Path(tmp_path) / self.log_file_name
        logger = FileCommandLogger(
            metadata,
            LoggerOptions(),
            tmp_path,
            output_file,
            True,
            False,
            False
        )

        # Run the test
        stdout = StringIO("foo")
        logger.log(stdout, None)
        logger.log_results(self.result, [])

        # Validate results
        assert not output_file.read_text().strip()


    def test_no_output_if_no_file_flag(self, tmp_path: Any):
        # Set up the logger
        metadata = CommandMetadata("cmd", ["arg1", "arg2"], CommandFlags.NO_FILE)
        output_file = Path(tmp_path) / self.log_file_name
        logger = FileCommandLogger(
            metadata,
            LoggerOptions(),
            tmp_path,
            output_file,
            True,
            False,
            False
        )

        # Run the test
        stdout = StringIO("foo")
        logger.log(stdout, None)
        logger.log_results(self.result, [])

        # Validate results
        assert not output_file.read_text().strip()


    def test_has_output_if_no_console_flag(self, tmp_path: Any):
        # Set up the logger
        metadata = CommandMetadata("cmd", ["arg1", "arg2"], CommandFlags.NO_CONSOLE)
        output_file = Path(tmp_path) / self.log_file_name
        logger = FileCommandLogger(
            metadata,
            LoggerOptions(),
            tmp_path,
            output_file,
            True,
            False,
            False
        )

        # Run the test
        stdout = StringIO("foo")
        logger.log(stdout, None)
        logger.log_results(self.result, [])

        # Validate results
        assert output_file.read_text().strip()


    def test_logger_creates_parent_dirs(self, tmp_path: Any):
        # Set up the logger
        output_file = Path(tmp_path) / "foo" / "bar" / self.log_file_name
        logger = FileCommandLogger(
            self.metadata,
            LoggerOptions(),
            tmp_path,
            output_file,
            False,
            False,
            False
        )

        # Run the test
        stdout = StringIO("foo")
        logger.log(stdout, None)
        logger.log_results(self.result, [])

        # Validate results
        assert output_file.exists()


    def test_logger_captures_output(self, tmp_path: Any):
        # Set up the logger
        output_file = Path(tmp_path) / self.log_file_name
        logger = FileCommandLogger(
            self.metadata,
            LoggerOptions(),
            tmp_path,
            output_file,
            False,
            False,
            False
        )

        # Run the test
        stdout = StringIO("foo")
        logger.log(stdout, None)
        logger.log_results(self.result, [])

        # Validate results
        assert "foo" in logger.output


    def test_skip_results_output_if_logging_disabled(self, tmp_path: Any):
        # Set up the logger
        log_file_path = Path(tmp_path) / self.log_file_name
        logger = FileCommandLogger(
            self.metadata,
            LoggerOptions(),
            tmp_path,
            log_file_path,
            False,
            False,
            False
        )

        # Run the test
        logger.log_results(self.result, [])

        # Validate results
        assert not log_file_path.read_text().strip()


    def test_custom_header(self, tmp_path: Any):
        # Set up the logger
        log_file_path = Path(tmp_path) / self.log_file_name
        header = "foobar"
        length = 2
        logger = FileCommandLogger(
            self.metadata,
            LoggerOptions(
                cmd_header_banner_char=header,
                cmd_header_banner_width=length
            ),
            tmp_path,
            log_file_path,
            False,
            True,
            False
        )

        # Run the test
        logger.log_results(self.result, [])

        # Validate results
        assert header * length in log_file_path.read_text()


    def test_custom_footer(self, tmp_path: Any):
        # Set up the logger
        log_file_path = Path(tmp_path) / self.log_file_name
        footer = "foobar"
        length = 2
        logger = FileCommandLogger(
            self.metadata,
            LoggerOptions(
                cmd_footer_banner_char=footer,
                cmd_footer_banner_width=length
            ),
            tmp_path,
            log_file_path,
            False,
            False,
            True
        )

        # Run the test
        logger.log_results(self.result, [])

        # Validate results
        assert footer * length in log_file_path.read_text()
