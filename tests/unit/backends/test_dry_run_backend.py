from pathlib import Path
from pyshell.backends.dry_run_backend import DryRunBackend
from pyshell.core.command_metadata import CommandMetadata
from pyshell.logging.null_command_logger import NullCommandLogger

def test_run_echo():
    cmd = ["echo", "foo"]
    cwd = "/foo/bar"

    backend = DryRunBackend()
    result = backend.run(
        CommandMetadata(
            cmd[0],
            cmd[1:]
        ),
        Path(cwd),
        NullCommandLogger()
    )
    assert result.command == cmd[0]
    assert result.args == cmd[1:]
    assert result.full_command == " ".join(cmd)
    assert result.cwd == str(cwd)
    assert result.output == ""
    assert result.exit_code == 0
    assert result.success


def test_run_invalid_cmd():
    cmd = ["invalid_cmd"]
    cwd = "/foo/bar"

    backend = DryRunBackend()
    result = backend.run(
        CommandMetadata(
            cmd[0],
            cmd[1:]
        ),
        Path(cwd),
        NullCommandLogger()
    )
    assert result.command == cmd[0]
    assert result.args == cmd[1:]
    assert result.full_command == " ".join(cmd)
    assert result.cwd == str(cwd)
    assert result.output == ""

    # The dry run backend should assume that all commands succeed
    assert result.exit_code == 0
    assert result.success
