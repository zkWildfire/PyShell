from pathlib import Path
from pyshell import PyShell, PyShellOptions, AbortOnFailure, NativeBackend, \
    NullFileLogger
from pyshell.shell.ls_command import LsCommand

def test_ls_command_with_no_arg():
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AbortOnFailure(),
        PyShellOptions(),
        cwd=Path(__file__).parent
    )

    # Run some commands
    cmd = LsCommand()
    result = cmd(pyshell)
    assert result.success

    # Verify that the output is correct
    curr_file = Path(__file__).name
    assert curr_file in result.output


def test_ls_command_with_arg():
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AbortOnFailure(),
        PyShellOptions(),
        cwd=Path(__file__).parent
    )

    # Run some commands
    cmd = LsCommand(Path(__file__).parent)
    result = cmd(pyshell)
    assert result.success

    # Verify that the output is correct
    curr_file = Path(__file__).name
    assert curr_file in result.output
