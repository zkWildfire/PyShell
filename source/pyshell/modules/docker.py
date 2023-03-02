from pathlib import Path
from pyshell.core.command_flags import CommandFlags
from pyshell.core.command_result import CommandResult
from pyshell.core.pyshell import PyShell
from pyshell.docker.exec_command import ExecCommand
from pyshell.docker.ps_command import PsCommand
from pyshell.docker.pull_command import PullCommand
from pyshell.docker.rm_command import RmCommand
from pyshell.docker.run_command import RunCommand
from pyshell.docker.start_command import StartCommand
from pyshell.docker.stop_command import StopCommand
from pyshell.modules.module import IModule
from typing import Dict, List, Optional

class Docker(IModule):
    """
    Module that provides access to docker commands.
    @ingroup modules
    @ingroup docker
    """
    @staticmethod
    def exec(
        container: str,
        cmd: str,
        args: str | List[str] | None = None,
        workdir: Optional[str] = None,
        user: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        env_file: Optional[str] = None,
        use_sudo: bool = False,
        cmd_flags: CommandFlags = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `docker exec` on the specified container.
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
        @param pyshell PyShell instance to execute the command via.
        @param cmd_flags The flags to set for the command.
        @return The results of running `docker exec`.
        """
        return ExecCommand(
            container,
            cmd,
            args,
            workdir,
            user,
            env,
            env_file,
            use_sudo,
            cmd_flags
        )(pyshell)


    @staticmethod
    def ps(
        show_all: bool = False,
        use_sudo: bool = False,
        cmd_flags: CommandFlags = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `docker ps`.
        @param show_all Whether to show all containers.
        @param use_sudo Whether to use `sudo` when running the command.
        @param pyshell PyShell instance to execute the command via.
        @param cmd_flags The flags to set for the command.
        @return The results of running `docker ps`.
        """
        return PsCommand(show_all, use_sudo, cmd_flags)(pyshell)


    @staticmethod
    def pull(
        image: str,
        use_sudo: bool = False,
        cmd_flags: CommandFlags = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `docker pull`.
        @param image The image to pull.
        @param use_sudo Whether to use `sudo` when running the command.
        @param pyshell PyShell instance to execute the command via.
        @param cmd_flags The flags to set for the command.
        @return The results of running `docker pull`.
        """
        return PullCommand(image, use_sudo, cmd_flags)(pyshell)


    @staticmethod
    def rm(
        container: str,
        force: bool = False,
        use_sudo: bool = False,
        cmd_flags: CommandFlags = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `docker rm`.
        @param container The container to remove.
        @param force Whether to force the removal of the container.
        @param use_sudo Whether to use `sudo` when running the command.
        @param pyshell PyShell instance to execute the command via.
        @param cmd_flags The flags to set for the command.
        @return The results of running `docker rm`.
        """
        return RmCommand(container, force, use_sudo, cmd_flags)(pyshell)


    @staticmethod
    def run(
        image: str,
        command: Optional[str] = None,
        args: str | List[str] | None = None,
        container_name: Optional[str] = None,
        detach: bool = False,
        interactive: bool = False,
        tty: bool = False,
        user: Optional[str] = None,
        workdir: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        env_file: str | Path | None = None,
        volumes: Optional[List[str]] = None,
        remove_after: bool = False,
        use_sudo: bool = False,
        cmd_flags: CommandFlags = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `docker run`.
        @param image The image to run.
        @param command Command to run inside the container.
        @param args Arguments to pass to the command.
        @param container_name The name to give the container.
        @param detach Whether to run the container in detached mode.
        @param interactive Whether to run the container in interactive mode.
        @param tty Whether to run the container with a TTY.
        @param user The user to run the container as.
        @param workdir The working directory to use when running the container.
        @param env The environment variables to set when running the container.
        @param env_file The path to a file containing environment variables to
          set when running the container.
        @param volumes The volumes to mount when running the container.
        @param remove_after Whether to remove the container after it exits.
        @param use_sudo Whether to use `sudo` when running the command.
        @param pyshell PyShell instance to execute the command via.
        @param cmd_flags The flags to set for the command.
        @return The results of running `docker run`.
        """
        return RunCommand(
            image,
            command,
            args,
            container_name,
            detach,
            interactive,
            tty,
            user,
            workdir,
            env,
            env_file,
            volumes,
            remove_after,
            use_sudo,
            cmd_flags
        )(pyshell)


    @staticmethod
    def start(
        container: str,
        use_sudo: bool = False,
        cmd_flags: CommandFlags = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `docker start`.
        @param container Name or ID of the container to start.
        @param use_sudo Whether to use `sudo` when running the command.
        @param pyshell PyShell instance to execute the command via.
        @param cmd_flags The flags to set for the command.
        @return The results of running `docker start`.
        """
        return StartCommand(
            container,
            use_sudo,
            cmd_flags
        )(pyshell)


    @staticmethod
    def stop(
        container: str,
        use_sudo: bool = False,
        cmd_flags: CommandFlags = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `docker stop`.
        @param container The container to stop.
        @param use_sudo Whether to use `sudo` when running the command.
        @param pyshell PyShell instance to execute the command via.
        @param cmd_flags The flags to set for the command.
        @return The results of running `docker stop`.
        """
        return StopCommand(container, use_sudo, cmd_flags)(pyshell)
