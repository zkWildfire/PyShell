import os
from pyshell import PyShell, KeepGoing
from pyshell.modules.docker import Docker

def test_pull_command():
    # Initialize a PyShell instance for running commands
    pyshell = PyShell()

    # If this is being run in a dev container or on a CI server, `use_sudo`
    #   must be set to True
    use_sudo = os.getenv("DEV_CONTAINER") == "1"

    # Run the pull command
    result = Docker.pull("hello-world", pyshell=pyshell, use_sudo=use_sudo)
    assert result.success


def test_pull_nonexistent_image():
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(error_handler=KeepGoing())

    # If this is being run in a dev container or on a CI server, `use_sudo`
    #   must be set to True
    use_sudo = os.getenv("DEV_CONTAINER") == "1"

    # Run the pull command
    result = Docker.pull(
        "nonexistent-image",
        pyshell=pyshell,
        use_sudo=use_sudo
    )
    assert not result.success
