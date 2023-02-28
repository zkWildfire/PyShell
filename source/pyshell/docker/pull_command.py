from pyshell.core.command_flags import CommandFlags
from pyshell.docker.docker_command import DockerCommand

class PullCommand(DockerCommand):
    """
    Defines a command that runs `docker pull`.
    @ingroup commands
    @ingroup docker
    """
    def __init__(self,
        image: str,
        use_sudo: bool = False,
        cmd_flags: CommandFlags = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param image The docker image to pull.
        @param use_sudo Whether to use `sudo` when running the command.
        @param cmd_flags The flags to set for the command.
        """
        super().__init__(
            "pull",
            image,
            use_sudo=use_sudo,
            cmd_flags=cmd_flags
        )
