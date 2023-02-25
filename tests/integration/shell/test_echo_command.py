from pyshell import PyShell, PyShellOptions, AbortOnFailure, NativeBackend, \
    NullFileLogger
from pyshell.shell.echo_command import EchoCommand

def test_echo_command():
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AbortOnFailure(),
        PyShellOptions()
    )

    # Run the commands
    msg = "foo bar"
    cmd = EchoCommand(msg)
    result = cmd(pyshell)
    assert result.success

    # Verify that the output is correct
    assert result.output == f"{msg}\n"
