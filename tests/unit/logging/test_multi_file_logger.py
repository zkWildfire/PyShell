import os
from pathlib import Path
from pyshell.core.command_result import CommandResult
from pyshell.logging.multi_file_logger import MultiFileLogger
from typing import Any

def test_log_path_matches_ctor_arg(tmp_path: Any):
    log_path = Path.joinpath(tmp_path, "foo/bar")
    logger = MultiFileLogger(log_path)
    assert logger.output_dir == log_path


def test_log_writes_to_file(tmp_path: Any):
    log_path = tmp_path / "logs"
    logger = MultiFileLogger(log_path)
    logger.log(CommandResult(
        "foo",
        [],
        os.getcwd(),
        "bar",
        0,
        True
    ))
    assert (log_path / "1-foo.log").read_text() == "bar\n"


def test_log_multiple_commands(tmp_path: Any):
    log_path = tmp_path / "logs"
    logger = MultiFileLogger(log_path)
    logger.log(CommandResult("foo", [], "foo", "FOO", 0, True))
    logger.log(CommandResult("bar", [], "bar", "BAR", 0, True))
    logger.log(CommandResult(
        "foo",
        [],
        os.getcwd(),
        "FOO",
        0,
        True
    ))
    logger.log(CommandResult(
        "bar",
        [],
        os.getcwd(),
        "BAR",
        0,
        True
    ))
    assert (log_path / "1-foo.log").read_text() == "FOO\n"
    assert (log_path / "2-bar.log").read_text() == "BAR\n"


def test_log_command_given_by_path(tmp_path: Any):
    log_path = tmp_path / "logs"
    logger = MultiFileLogger(log_path)
    logger.log(CommandResult(
        "/usr/bin/foo",
        [],
        os.getcwd(),
        "FOO",
        0,
        True
    ))
    assert (log_path / "1-foo.log").read_text() == "FOO\n"


def test_log_cmd_header(tmp_path: Any):
    # Constants
    log_path = tmp_path / "logs"
    cmd = "foo"
    cwd = "/cwd"

    # Run the test
    logger = MultiFileLogger(log_path, print_cmd_header=True)
    logger.log(CommandResult(
        cmd,
        [],
        cwd,
        "FOO",
        0,
        True
    ))

    # Validate results
    log_file = log_path / "1-foo.log"
    assert log_file.exists()

    contents = log_file.read_text()
    assert cmd in contents
    assert cwd in contents


def test_log_cmd_footer(tmp_path: Any):
    # Constants
    log_path = tmp_path / "logs"
    cmd = "foo"
    cwd = "/cwd"
    exit_code = 123

    # Run the test
    logger = MultiFileLogger(log_path, print_cmd_footer=True)
    logger.log(CommandResult(
        cmd,
        [],
        cwd,
        "FOO",
        exit_code,
        True
    ))

    # Validate results
    log_file = log_path / "1-foo.log"
    assert log_file.exists()

    contents = log_file.read_text()
    assert cmd in contents
    assert cwd in contents
    assert str(exit_code) in contents
