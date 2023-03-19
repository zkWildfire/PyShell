from pathlib import Path
from pyshell.commands.command_flags import CommandFlags
from pyshell.docker.docker_command import DockerCommand
from typing import List

class BuildCommand(DockerCommand):
    """
    Defines a command that runs `docker build`.
    @ingroup commands
    @ingroup docker
    """
    def __init__(self,
        tag: str,
        dockerfile: str | Path,
        context: str | Path = ".",
        use_sudo: bool = False,
        cmd_flags: int = CommandFlags.STANDARD,
        **kwargs: str):
        """
        Initializes the command.
        @param tag The tag to assign to the image.
        @param dockerfile The path to the Dockerfile to use.
        @param context The path to pass to `docker build` as the build context
          path.
        @param use_sudo Whether to use `sudo` when running the command.
        @param cmd_flags The flags to set for the command.
        @param kwargs Additional arguments to be passed using the `--build-arg`
          flag.
        """
        # Build the command to execute
        args: List[str] = [
            "-t",
            tag,
            "-f",
            str(dockerfile)
        ]
        for key, value in kwargs.items():
            args.append("--build-arg")
            args.append(f"{key}={value}")
        args.append(str(context))

        super().__init__(
            "build",
            args,
            use_sudo=use_sudo,
            cmd_flags=cmd_flags
        )
