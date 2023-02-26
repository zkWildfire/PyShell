import os
from pathlib import Path
from pyshell.core.command_metadata import CommandMetadata
from pyshell.core.command_result import CommandResult
from pyshell.logging.single_file_logger import SingleFileLogger
from typing import Any

def test_file_path_matches_ctor_arg(tmp_path: Any):
    file_path = Path.joinpath(tmp_path, "foo/bar.log")
    logger = SingleFileLogger(file_path)
    assert logger.file_path == file_path


def test_log_writes_to_file(tmp_path: Any):
    file_path = tmp_path / "log.txt"
    logger = SingleFileLogger(file_path)
    logger.log(CommandResult(
        CommandMetadata("foo", []),
        os.getcwd(),
        "bar",
        0,
        False
    ))
    assert file_path.read_text() == "bar\n"


def test_log_multiple_commands(tmp_path: Any):
    file_path = tmp_path / "log.txt"
    logger = SingleFileLogger(file_path)
    logger.log(CommandResult(
        CommandMetadata("foo", []),
        os.getcwd(),
        "FOO",
        0,
        False
    ))
    logger.log(CommandResult(
        CommandMetadata("bar", []),
        os.getcwd(),
        "BAR",
        0,
        False
    ))
    assert file_path.read_text() == "FOO\nBAR\n"


def test_log_cmd_header(tmp_path: Any):
    # Constants
    file_path = tmp_path / "log.txt"
    cmd = "foo"
    cwd = "/cwd"

    # Run the test
    logger = SingleFileLogger(file_path, print_cmd_header=True)
    logger.log(CommandResult(
        CommandMetadata(cmd, []),
        cwd,
        "FOO",
        0,
        False
    ))

    # Validate results
    contents = file_path.read_text()
    assert cmd in contents
    assert cwd in contents


def test_log_cmd_footer(tmp_path: Any):
    # Constants
    file_path = tmp_path / "log.txt"
    cmd = "foo"
    cwd = "/cwd"
    exit_code = 123

    # Run the test
    logger = SingleFileLogger(file_path, print_cmd_footer=True)
    logger.log(CommandResult(
        CommandMetadata(cmd, []),
        cwd,
        "FOO",
        exit_code,
        False
    ))

    # Validate results
    contents = file_path.read_text()
    assert cmd in contents
    assert cwd in contents
    assert str(exit_code) in contents
