import os
from pathlib import Path
from pyshell.backends.native_backend import NativeBackend
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.logging.console_command_logger import ConsoleCommandLogger
from pyshell.logging.logger_options import LoggerOptions
from pyshell.logging.null_command_logger import NullCommandLogger
from pyshell.logging.split_command_logger import SplitCommandLogger

def test_run_echo():
    cmd = ["echo", "foo"]
    cwd = os.getcwd()

    backend = NativeBackend()
    metadata = CommandMetadata(
        cmd[0],
        cmd[1:]
    )
    result = backend.run(
        metadata,
        Path(os.getcwd()),
        ConsoleCommandLogger(
            metadata,
            LoggerOptions(),
            Path.cwd()
        )
    )
    assert result.command == cmd[0]
    assert result.args == cmd[1:]
    assert result.full_command == " ".join(cmd)
    assert result.cwd == str(cwd)
    assert result.output == "foo\n"
    assert result.exit_code == 0
    assert result.success


def test_run_in_different_cwd():
    cmd = ["echo", "foo"]
    cwd = Path(os.getcwd()).parent

    backend = NativeBackend()
    result = backend.run(
        CommandMetadata(
            cmd[0],
            cmd[1:]
        ),
        Path(cwd),
        NullCommandLogger()
    )
    assert result.cwd == str(cwd)


def test_backend_adds_final_newline_if_missing():
    cmd = ["echo", "-n", "foo"]

    backend = NativeBackend()
    metadata = CommandMetadata(
        cmd[0],
        cmd[1:]
    )
    result = backend.run(
        metadata,
        Path.cwd(),
        ConsoleCommandLogger(
            metadata,
            LoggerOptions(),
            Path.cwd()
        )
    )
    assert result.output == "foo\n"


def test_use_split_streams():
    # Set up the command to run
    msg = "foo"
    cmd = ["bash", "-c", f"echo {msg} >&2"]
    cwd = os.getcwd()
    metadata = CommandMetadata(
        cmd[0],
        cmd[1:]
    )

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
        metadata,
        LoggerOptions(),
        Path.cwd(),
        on_stdout
    )
    stderr_logger = ConsoleCommandLogger(
        metadata,
        LoggerOptions(),
        Path.cwd(),
        on_stderr
    )
    logger = SplitCommandLogger(stdout_logger, stderr_logger)

    backend = NativeBackend()
    result = backend.run(
        metadata,
        Path(cwd),
        logger
    )

    assert result.success
    assert not stdout_output
    assert msg in stderr_output
