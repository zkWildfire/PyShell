import os
from pyshell.core.pyshell import PyShell
from pyshell.modules.docker import Docker

def test_remove_image():
    pyshell = PyShell()

    # If this is being run in a dev container or on a CI server, `use_sudo`
    #   must be set to True
    use_sudo = os.getenv("DEV_CONTAINER") == "1"

    # Pull an image to be removed
    tag = "hello-world:latest"
    pull_result = Docker.pull(
        image=tag,
        use_sudo=use_sudo,
        pyshell=pyshell
    )

    # If this command fails, don't bother running the rmi command
    assert pull_result.success

    # Attempt to remove the image
    rmi_result = Docker.rmi(tag=tag, use_sudo=use_sudo, pyshell=pyshell)
    assert rmi_result.success
