from pyshell.core.command_flags import CommandFlags
from pyshell.docker.docker_command import DockerCommand
from typing import List, Optional

class StartCommand(DockerCommand):
    """
    Defines a command that runs `docker start`.
    @ingroup commands
    @ingroup docker
    """
    def __init__(self,
        image_name: str,
        container_name: Optional[str] = None,
        detach: bool = False,
        use_sudo: bool = False,
        cmd_flags: CommandFlags = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param image_name The name of the image to start.
        @param container_name The name to assign to the container.
        @param detach Whether to start the container in detached mode.
        @param use_sudo Whether to use `sudo` when running the command.
        @param cmd_flags The flags to set for the command.
        """
        # Build the command to execute
        args: List[str] = []
        if detach:
            args.append("-d")
        if container_name is not None:
            args.append("--name")
            args.append(container_name)
        args.append(image_name)

        super().__init__(
            "start",
            container_name,
            use_sudo=use_sudo,
            cmd_flags=cmd_flags
        )
