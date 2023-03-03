from pyshell.commands.command_flags import CommandFlags
from pyshell.docker.docker_command import DockerCommand

class PsCommand(DockerCommand):
    """
    Defines a command that runs `docker ps`.
    @ingroup commands
    @ingroup docker
    """
    def __init__(self,
        show_all: bool = False,
        use_sudo: bool = False,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param show_all Whether to show all containers. Enables the `-a` flag.
        @param use_sudo Whether to use `sudo` when running the command.
        @param cmd_flags The flags to set for the command.
        """
        args = ["-a"] if show_all else []

        super().__init__(
            "ps",
            args,
            use_sudo=use_sudo,
            cmd_flags=cmd_flags
        )
