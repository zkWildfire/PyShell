from pathlib import Path
from pyshell.core.command_flags import CommandFlags
from pyshell.docker.docker_command import DockerCommand
from typing import Dict, List, Optional, Sequence

class RunCommand(DockerCommand):
    """
    Defines a command that runs `docker run`.
    @ingroup commands
    @ingroup docker
    """
    def __init__(self,
        image: str,
        command: Optional[str] = None,
        args: str | Sequence[str] | None = None,
        container_name: Optional[str] = None,
        detach: bool = False,
        interactive: bool = False,
        tty: bool = False,
        user: Optional[str] = None,
        workdir: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        env_file: str | Path | None = None,
        volumes: Optional[Sequence[str]] = None,
        ports: str | Sequence[str] | None = None,
        remove_after: bool = False,
        use_sudo: bool = False,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param image Name of the image to run.
        @param command Command to run inside the container.
        @param args Arguments to pass to the command.
        @param container_name Name of the container to create.
        @param detach Whether to run the container in detached mode.
        @param interactive Whether to run the container in interactive mode.
        @param tty Whether to allocate a pseudo-TTY.
        @param user User to run the container as.
        @param workdir Working directory to use inside the container.
        @param env Environment variables to set inside the container.
        @param env_file Path to a file containing environment variables to set
          inside the container.
        @param volumes Volumes to mount inside the container.
        @param ports A list of ports to expose. Each string in this argument
          will be passed to the `--publish` option of the `docker run` command.
        @param remove_after Whether to remove the container after it exits.
        @param use_sudo Whether to use `sudo` when running the command.
        @param cmd_flags The flags to set for the command.
        """
        # Build the command to execute
        cmd_args: List[str] = []
        if container_name:
            cmd_args.extend(["--name", container_name])
        if detach:
            cmd_args.append("-d")
        if interactive:
            cmd_args.append("-i")
        if tty:
            cmd_args.append("-t")
        if user:
            cmd_args.extend(["--user", user])
        if workdir:
            cmd_args.extend(["--workdir", workdir])
        if env:
            for key, value in env.items():
                cmd_args.extend(["-e", f"{key}={value}"])
        if env_file:
            cmd_args.extend(["--env-file", str(env_file)])
        if volumes:
            for volume in volumes:
                cmd_args.extend(["-v", volume])
        if ports:
            if isinstance(ports, str):
                ports = [ports]
            for port in ports:
                cmd_args.extend(["--publish", port])
        if remove_after:
            cmd_args.append("--rm")
        cmd_args.append(image)
        if command:
            cmd_args.append(command)
        if args:
            if isinstance(args, str):
                cmd_args.append(args)
            else:
                cmd_args.extend(args)

        super().__init__(
            "run",
            cmd_args,
            use_sudo=use_sudo,
            cmd_flags=cmd_flags
        )
