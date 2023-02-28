import os
from pyshell import PyShell
from pyshell.modules.docker import Docker

def test_ps_command():
    # Initialize a PyShell instance for running commands
    pyshell = PyShell()

    # If this is being run in a dev container or on a CI server, `use_sudo`
    #   must be set to True
    use_sudo = os.getenv("DEV_CONTAINER") == "1"

    # Run the ps command
    result = Docker.ps(pyshell=pyshell, use_sudo=use_sudo)
    assert result.success

    # Verify that the output is correct
    assert "CONTAINER ID" in result.output
