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
    logger.log(CommandResult("foo", [], "foo", "bar", 0, True))
    assert (log_path / "1-foo.log").read_text() == "bar\n"


def test_log_command_to_file(tmp_path: Any):
    log_path = tmp_path / "logs"
    logger = MultiFileLogger(log_path, print_cmds=True)
    logger.log(CommandResult("foo", [], "foo", "", 0, True))
    assert (log_path / "1-foo.log").read_text() == \
        "[PyShell] Running command: foo\n\n"


def test_skip_logging_command_to_file(tmp_path: Any):
    log_path = tmp_path / "logs"
    logger = MultiFileLogger(log_path, print_cmds=False)
    logger.log(CommandResult("foo", [], "foo", "", 0, True))
    assert (log_path / "1-foo.log").read_text() == "\n"


def test_log_multiple_commands(tmp_path: Any):
    log_path = tmp_path / "logs"
    logger = MultiFileLogger(log_path, print_cmds=False)
    logger.log(CommandResult("foo", [], "foo", "FOO", 0, True))
    logger.log(CommandResult("bar", [], "bar", "BAR", 0, True))
    assert (log_path / "1-foo.log").read_text() == "FOO\n"
    assert (log_path / "2-bar.log").read_text() == "BAR\n"


def test_log_command_given_by_path(tmp_path: Any):
    log_path = tmp_path / "logs"
    logger = MultiFileLogger(log_path, print_cmds=False)
    logger.log(CommandResult("/usr/bin/foo", [], "/usr/bin/foo", "FOO", 0, True))
    assert (log_path / "1-foo.log").read_text() == "FOO\n"
