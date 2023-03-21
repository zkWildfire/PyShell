from datetime import datetime
from pathlib import Path
from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.async_command_result import AsyncCommandResult
from pyshell.logging.console_command_logger import ConsoleCommandLogger
from pyshell.logging.logger_options import LoggerOptions
from pyshell.logging.null_command_logger import NullCommandLogger
import os
import subprocess

def test_wait_blocks_until_process_exits():
    """
    Test that wait() blocks until the process exits.
    """
    target_duration_sec = 5
    start_time = datetime.utcnow()
    proc = subprocess.Popen(
        ["sleep", str(target_duration_sec)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    result = AsyncCommandResult(
        proc,
        NullCommandLogger(),
        CommandMetadata("sleep", ["1"]),
        os.getcwd(),
        datetime.utcnow(),
        "foo"
    )

    # Accessing any value dependent on the process exiting should block until
    #   the process exits.
    result.exit_code

    end_time = datetime.utcnow()
    duration = end_time - start_time

    assert duration.total_seconds() >= target_duration_sec


def test_wait_returns_immediately_if_process_already_exited():
    """
    Test that wait() returns immediately if the process has already exited.
    """
    target_duration_sec = 1
    proc = subprocess.Popen(
        ["sleep", str(target_duration_sec)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    result = AsyncCommandResult(
        proc,
        NullCommandLogger(),
        CommandMetadata("sleep", ["1"]),
        os.getcwd(),
        datetime.utcnow(),
        "foo"
    )

    # Wait for the process to exit
    while proc.poll() is None:
        pass

    # Accessing any value dependent on the process exiting should not block
    #   since the process has already exited.
    start_time = datetime.utcnow()
    result.exit_code
    end_time = datetime.utcnow()
    duration = end_time - start_time

    assert duration.total_seconds() < target_duration_sec


def test_successful_command_properties_match_expected():
    """
    Test that the command properties match the expected values.
    """
    cmd = "echo"
    args = ["foo"]
    backend = "backend"
    metadata = CommandMetadata(cmd, args, CommandFlags.ASYNC)

    proc = subprocess.Popen(
        [cmd] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    result = AsyncCommandResult(
        proc,
        ConsoleCommandLogger(
            metadata,
            LoggerOptions(),
            Path(os.getcwd())
        ),
        metadata,
        os.getcwd(),
        datetime.utcnow(),
        backend
    )
    result.wait()

    assert bool(result)
    assert result.command == cmd
    assert result.args == args
    assert result.cwd == os.getcwd()
    assert args[0] in result.output
    assert result.exit_code == 0
    assert result.success
    assert not result.error
    assert not result.skipped
    assert cmd in result.full_command
    assert args[0] in result.full_command
    assert result.start_time_utc <= result.end_time_utc
    assert result.start_time_local <= result.end_time_local
    assert result.duration_milliseconds >= 0
    assert result.duration_seconds >= 0
    assert result.duration_minutes >= 0
    assert result.backend == backend


def test_failed_command_properties_match_expected():
    """
    Test that the command properties match the expected values.
    """
    cmd = "ls"
    args = ["/foo/bar"]
    backend = "foo"

    proc = subprocess.Popen(
        [cmd] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    result = AsyncCommandResult(
        proc,
        NullCommandLogger(),
        CommandMetadata(cmd, args),
        os.getcwd(),
        datetime.utcnow(),
        backend
    )
    result.wait()

    assert not bool(result)
    assert result.command == cmd
    assert result.args == args
    assert result.cwd == os.getcwd()
    assert result.exit_code != 0
    assert not result.success
    assert result.error
    assert not result.skipped
    assert cmd in result.full_command
    assert args[0] in result.full_command
    assert result.start_time_utc <= result.end_time_utc
    assert result.start_time_local <= result.end_time_local
    assert result.backend == backend
