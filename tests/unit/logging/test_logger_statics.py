from datetime import datetime, timedelta
import os
from pathlib import Path
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.command_result import CommandResult
from pyshell.logging.logger_statics import LoggerStatics


def test_write_header():
    cmd = "foo"
    args = ["bar", "baz"]
    metadata = CommandMetadata(
        cmd,
        args
    )
    cwd = Path.cwd()
    output = ""

    def write_callback(data: str):
        nonlocal output
        output += data

    LoggerStatics.write_command_header(metadata, cwd, write_callback)

    assert "Running command" in output
    assert cmd in output
    for arg in args:
        assert arg in output
    assert "cwd" in output
    assert str(cwd) in output


def test_write_footer():
    cmd = "foo"
    args = ["bar", "baz"]
    exit_code = 1
    cwd = os.getcwd()
    start_time = datetime.now()
    end_time = datetime.now() + timedelta(seconds=1)
    backend = "FOOBAR"

    result = CommandResult(
        cmd,
        args,
        cwd,
        "",
        exit_code,
        False,
        start_time,
        end_time,
        backend
    )

    output = ""
    def write_callback(data: str):
        nonlocal output
        output += data

    LoggerStatics.write_command_footer(result, write_callback)

    assert "Executed command" in output
    assert "Backend" in output
    assert backend in output
    assert "cwd" in output
    assert cwd in output
    assert "Command exited with code" in output
    assert str(exit_code) in output
    assert "Start time" in output
    assert "End time" in output
    assert "Duration" in output
