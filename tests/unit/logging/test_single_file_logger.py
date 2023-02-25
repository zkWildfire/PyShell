import os
from pathlib import Path
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
        "foo",
        [],
        os.getcwd(),
        "bar",
        0,
        True
    ))
    assert file_path.read_text() == "bar\n"


def test_log_multiple_commands(tmp_path: Any):
    file_path = tmp_path / "log.txt"
    logger = SingleFileLogger(file_path)
    logger.log(CommandResult(
        "foo",
        [],
        os.getcwd(),
        "FOO",
        0,
        True
    ))
    logger.log(CommandResult(
        "foo",
        [],
        os.getcwd(),
        "BAR",
        0,
        True
    ))
    assert file_path.read_text() == "FOO\nBAR\n"
