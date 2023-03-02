from pyshell.core.command_flags import CommandFlags
from pyshell.core.external_command import ExternalCommand
from typing import List, Optional

class DockerCommand(ExternalCommand):
    """
    Class used to run docker commands.
    This class is used as a base class for the built-in docker command classes.
    @ingroup commands
    @ingroup docker
    """
    def __init__(self,
        docker_cmd: Optional[str],
        args: str | List[str] | None = None,
        use_sudo: bool = False,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param docker_cmd The docker command to run, e.g. `ps`, `pull`, etc.
          If this is `None`, then `args` will be passed to `docker` directly.
        @param args The arguments to pass to the `docker [cmd]` command.
        @param use_sudo Whether to use `sudo` when running the command.
        @param cmd_flags The flags to set for the command.
        """
        # Construct the command to execute
        cmd: List[str] = []
        if use_sudo:
            cmd.append("sudo")
        cmd.append("docker")
        if docker_cmd is not None:
            cmd.append(docker_cmd)
        if not args:
            pass
        elif isinstance(args, str):
            cmd.append(args)
        else:
            cmd.extend(args)

        super().__init__(
            cmd[0],
            cmd[1:],
            cmd_flags=cmd_flags
        )
