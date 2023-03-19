from pyshell.commands.command_flags import CommandFlags
from pyshell.docker.docker_command import DockerCommand
from typing import List

class RmiCommand(DockerCommand):
    """
    Defines a command that runs `docker rmi`.
    @ingroup commands
    @ingroup docker
    """
    def __init__(self,
        tag: str,
        use_sudo: bool = False,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param tag The tag of the image to remove.
        @param use_sudo Whether to use `sudo` when running the command.
        @param cmd_flags The flags to set for the command.
        """
        # Build the command to execute
        args: List[str] = [tag]

        super().__init__(
            "rmi",
            args,
            use_sudo=use_sudo,
            cmd_flags=cmd_flags
        )
