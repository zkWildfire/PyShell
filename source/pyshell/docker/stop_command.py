from pyshell.core.command_flags import CommandFlags
from pyshell.docker.docker_command import DockerCommand

class StopCommand(DockerCommand):
    """
    Defines a command that runs `docker stop`.
    @ingroup commands
    @ingroup docker
    """
    def __init__(self,
        container_name: str,
        use_sudo: bool = False,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param container_name The name of the container to stop.
        @param use_sudo Whether to use `sudo` when running the command.
        @param cmd_flags The flags to set for the command.
        """
        super().__init__(
            "stop",
            container_name,
            use_sudo=use_sudo,
            cmd_flags=cmd_flags
        )
