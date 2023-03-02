from pyshell import PyShell, PyShellOptions, AbortOnFailure, AllowAll, \
    NativeBackend, ConsoleLogger
from pyshell.modules.shell import Shell

def test_echo_command():
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        ConsoleLogger(),
        AllowAll(),
        AbortOnFailure(),
        PyShellOptions()
    )

    # Run the commands
    msg = "foo bar"
    result = Shell.echo(msg, pyshell=pyshell)
    assert result.success

    # Verify that the output is correct
    assert result.output == f"{msg}\n"
