import os
from pathlib import Path
from pyshell.backends.native_backend import NativeBackend
from pyshell.core.command_metadata import CommandMetadata

def test_run_echo():
    cmd = ["echo", "foo"]
    cwd = os.getcwd()

    backend = NativeBackend()
    result = backend.run(
        CommandMetadata(
            cmd[0],
            cmd[1:]
        ),
        Path(os.getcwd())
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
        Path(cwd)
    )
    assert result.cwd == str(cwd)


def test_backend_adds_final_newline_if_missing():
    cmd = ["echo", "-n", "foo"]
    cwd = os.getcwd()

    backend = NativeBackend()
    result = backend.run(
        CommandMetadata(
            cmd[0],
            cmd[1:]
        ),
        Path(cwd)
    )
    assert result.output == "foo\n"
