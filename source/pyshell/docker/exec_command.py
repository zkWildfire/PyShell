from pyshell.core.command_flags import CommandFlags
from pyshell.docker.docker_command import DockerCommand
from typing import Dict, List, Optional

class ExecCommand(DockerCommand):
    """
    Defines a command that runs `docker exec`.
    @ingroup commands
    @ingroup docker
    """
    def __init__(self,
        container: str,
        cmd: str,
        args: str | List[str] | None = None,
        workdir: Optional[str] = None,
        user: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        env_file: Optional[str] = None,
        use_sudo: bool = False,
        cmd_flags: CommandFlags = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param container Name or ID of the container to run the command in.
        @param cmd The command to run in the container.
        @param args The arguments to pass to the command.
        @param workdir The working directory in the container to use when
          running the command.
        @param user The user to run the command as in the container.
        @param env The environment variables to set when running the command.
        @param env_file The path to a file containing environment variables to
          set when running the command.
        @param use_sudo Whether to use `sudo` when running the command.
        @param cmd_flags The flags to set for the command.
        """
        # Build the command to execute
        exec_args: List[str] = []
        if workdir is not None:
            exec_args.append("-w")
            exec_args.append(workdir)
        if user is not None:
            exec_args.append("-u")
            exec_args.append(user)
        if env is not None:
            for key, value in env.items():
                exec_args.append("-e")
                exec_args.append(f"{key}={value}")
        if env_file is not None:
            exec_args.append("--env-file")
            exec_args.append(env_file)
        exec_args.append(container)
        exec_args.append(cmd)
        if not args:
            pass
        elif isinstance(args, str):
            exec_args.append(args)
        else:
            exec_args.extend(args)

        super().__init__(
            "run",
            exec_args,
            use_sudo=use_sudo,
            cmd_flags=cmd_flags
        )
