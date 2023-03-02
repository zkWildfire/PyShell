from pyshell.core.command_flags import CommandFlags
from pyshell.docker.docker_command import DockerCommand

class StartCommand(DockerCommand):
    """
    Defines a command that runs `docker start`.
    @ingroup commands
    @ingroup docker
    """
    def __init__(self,
        container: str,
        use_sudo: bool = False,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param container Name or ID of the container to start.
        @param use_sudo Whether to use `sudo` when running the command.
        @param cmd_flags The flags to set for the command.
        """
        super().__init__(
            "start",
            container,
            use_sudo=use_sudo,
            cmd_flags=cmd_flags
        )
