from pathlib import Path
from pyshell.backends.dry_run_backend import DryRunBackend
from pyshell.commands.command_metadata import CommandMetadata
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


def test_all_commands_recorded_in_order():
    cmd1 = ["echo", "foo"]
    cmd2 = ["echo", "bar"]
    cwd = "/foo/bar"

    backend = DryRunBackend()
    backend.run(
        CommandMetadata(
            cmd1[0],
            cmd1[1:]
        ),
        Path(cwd),
        NullCommandLogger()
    )
    backend.run(
        CommandMetadata(
            cmd2[0],
            cmd2[1:]
        ),
        Path(cwd),
        NullCommandLogger()
    )

    assert backend.commands == [" ".join(cmd1), " ".join(cmd2)]
