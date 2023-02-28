from pyshell.core.command_flags import CommandFlags
from pyshell.docker.docker_command import DockerCommand
from typing import List

class StartCommand(DockerCommand):
    """
    Defines a command that runs `docker start`.
    @ingroup commands
    @ingroup docker
    """
    def __init__(self,
        container: str,
        attach: bool = False,
        interactive: bool = False,
        use_sudo: bool = False,
        cmd_flags: CommandFlags = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param container Name or ID of the container to start.
        @param attach Whether to attach to the container.
        @param interactive Whether to attach to the container in interactive
          mode.
        @param use_sudo Whether to use `sudo` when running the command.
        @param cmd_flags The flags to set for the command.
        """
        # Build the command to execute
        args: List[str] = []
        if attach:
            args.append("-a")
        if interactive:
            args.append("-i")
        args.append(container)

        super().__init__(
            "start",
            args,
            use_sudo=use_sudo,
            cmd_flags=cmd_flags
        )
