from pyshell.commands.command_flags import CommandFlags
from pyshell.docker.docker_command import DockerCommand
from typing import List

class RmCommand(DockerCommand):
    """
    Defines a command that runs `docker rm`.
    @ingroup commands
    @ingroup docker
    """
    def __init__(self,
        container: str,
        force: bool = False,
        use_sudo: bool = False,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param container Name or ID of the container to remove.
        @param force Whether to force the removal of the container.
        @param use_sudo Whether to use `sudo` when running the command.
        @param cmd_flags The flags to set for the command.
        """
        # Build the command to execute
        args: List[str] = []
        if force:
            args.append("-f")
        args.append(container)

        super().__init__(
            "rm",
            args,
            use_sudo=use_sudo,
            cmd_flags=cmd_flags
        )
