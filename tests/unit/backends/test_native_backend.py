import os
from pathlib import Path
from pyshell.backends.native_backend import NativeBackend
from pyshell.core.command_metadata import CommandMetadata
from pyshell.logging.console_command_logger import ConsoleCommandLogger
from pyshell.logging.null_command_logger import NullCommandLogger

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
        ConsoleCommandLogger(metadata)
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
    cwd = os.getcwd()

    backend = NativeBackend()
    metadata = CommandMetadata(
        cmd[0],
        cmd[1:]
    )
    result = backend.run(
        metadata,
        Path(cwd),
        ConsoleCommandLogger(metadata)
    )
    assert result.output == "foo\n"
