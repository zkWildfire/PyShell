from pyshell.core.command_flags import CommandFlags
from pyshell.core.external_command import ExternalCommand
from typing import List

class DockerCommand(ExternalCommand):
    """
    Class used to run docker commands.
    This class is used as a base class for the built-in docker command classes.
    @ingroup commands
    @ingroup docker
    """
    def __init__(self,
        cmd: str,
        args: str | List[str] | None = None,
        use_sudo: bool = False,
        cmd_flags: CommandFlags = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param cmd The docker command to run, e.g. `ps`, `pull`, etc.
        @param args The arguments to pass to the `docker [cmd]` command.
        @param use_sudo Whether to use `sudo` when running the command.
        @param cmd_flags The flags to set for the command.
        """
        cmd = "docker"
        if args is None:
            args = []
        elif isinstance(args, str):
            args = [args]

        if use_sudo:
            args.insert(0, cmd)
            cmd = "sudo"

        super().__init__(
            cmd,
            args,
            cmd_flags=cmd_flags
        )
