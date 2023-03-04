from datetime import datetime
from pathlib import Path
from pyshell.backends.backend import IBackend
from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.command_result import CommandResult
from pyshell.core.pyshell import PyShell
from pyshell.logging.command_logger import ICommandLogger
from pyshell.logging.stream_config import StreamConfig
from pyshell.modules.docker import Docker
import subprocess
from time import sleep
from typing import Optional, Sequence

class DockerBackend(IBackend):
    """
    Backend that executes commands in a docker container.
    @ingroup backends
    """
    def __init__(self,
        pyshell: PyShell,
        image: str,
        container_name: Optional[str] = None,
        ports: str | Sequence[str] | None = None,
        use_sudo: bool = False,
        quiet: bool = True):
        """
        Initializes the backend.
        @param pyshell The pyshell instance to use when running docker commands
          to set up the backend. This must be an instance that is configured
          with a backend that will execute commands on the host system, e.g. the
          `NativeBackend` class.
        @param image The docker image to use.
        @param container_name The name of the container to use. If None, a
          random name will be generated.
        @param ports A list of ports to expose. Each string in this argument
          will be passed to the `--publish` option of the `docker run` command.
        @param use_sudo Whether to use `sudo` when running docker commands.
        @param quiet Whether to suppress the output of docker commands used to
          set up the backend.
        @throws RuntimeError Thrown if docker is not available or the image
          could not be pulled.
        """
        self._use_sudo = use_sudo
        self._host_pyshell = pyshell
        self._quiet_flag = CommandFlags.QUIET if quiet else CommandFlags.NONE
        self._cmd_flags = self._quiet_flag | CommandFlags.STANDARD
        self._container_name = container_name

        # Make sure that privileged docker commands can be run
        result = Docker.ps(
            use_sudo=use_sudo,
            cmd_flags=self._cmd_flags,
            pyshell=pyshell
        )
        if not result.success:
            # This is not easily testable on CI/CD systems; ignore it for coverage
            raise RuntimeError( # pragma: no cover
                "Docker is not available on this system."
            )

        # Pull the image
        result = Docker.pull(
            image,
            use_sudo=use_sudo,
            cmd_flags=self._cmd_flags,
            pyshell=pyshell
        )
        if not result.success:
            raise RuntimeError(
                f"Could not pull image '{image}'."
            )

        # Start the docker container
        result = Docker.run(
            image,
            container_name=container_name,
            interactive=True,
            tty=True,
            detach=True,
            ports=ports,
            remove_after=True,
            use_sudo=use_sudo,
            cmd_flags=self._cmd_flags,
            pyshell=pyshell
        )
        if not result.success:
            if container_name:
                error_msg = f"Could not start container '{container_name}'.\n"
            else:
                error_msg = f"Could not start container using image '{image}'.\n"
            error_msg += f"Docker output:\n{result.output}"
            raise RuntimeError(error_msg)

        # Store the docker container's ID
        self._docker_container_id = result.output.strip()
        assert self._docker_container_id

        # Make sure the container doesn't exit immediately
        # Note that `docker ps` will print the first 12 characters of the
        #   container ID, hence why `[:12]` is used here
        sleep(1)
        result = Docker.ps(
            use_sudo=use_sudo,
            cmd_flags=self._cmd_flags,
            pyshell=pyshell
        )
        if not self._docker_container_id[:12] in result.output:
            if container_name:
                error_msg = f"Container '{container_name}' exited immediately."
            else:
                error_msg = f"Container using image '{image}' exited immediately."
            raise RuntimeError(error_msg)


    @property
    def container_id(self) -> str:
        """
        The ID of the docker container.
        """
        return self._docker_container_id


    def run(self,
        metadata: CommandMetadata,
        cwd: Path,
        logger: ICommandLogger) -> CommandResult:
        """
        Runs the specified command on the backend.
        @param metadata Metadata for the command to run.
        @param cwd The working directory to use for the command. Will always be
          an absolute path.
        @param logger The logger to use for the command. The backend will invoke
          `logger.log()` but will not invoke `logger.log_results()`.
        @return The output of the command.
        """
        # Determine how stderr should be handled
        if logger.stream_config == StreamConfig.SPLIT_STREAMS:
            process_stderr = subprocess.PIPE
        else: # logger.stream_config == StreamConfig.MERGE_STREAMS:
            process_stderr = subprocess.STDOUT

        # Invoke the docker exec command directly via subprocess instead of
        #   using `ExecCommand` because `ExecCommand` expects arguments to be
        #   passed to it in specific parameters. Since the backend receives the
        #   command as a single string plus an args array, it's easier and
        #   significantly less error prone to just invoke the docker exec
        #   command directly.
        start_time = datetime.utcnow()
        process = subprocess.Popen(
            (["sudo"] if self._use_sudo else []) +
            [
                "docker",
                "exec",
                self._docker_container_id,
                metadata.command,
                *metadata.args
            ],
            stdout=subprocess.PIPE,
            stderr=process_stderr,
            cwd=cwd,
            universal_newlines=True
        )

        # The process's stderr is allowed to be null since it could be
        #   redirected, but the process's stdout must always be valid
        assert process.stdout

        # Process all output from the process
        while process.poll() is None:
            logger.log(process.stdout, process.stderr)

        # Process any remaining output from the process
        logger.log(process.stdout, process.stderr)

        # Make sure the returned output always ends with a newline
        output = logger.output
        if not output.endswith("\n"):
            output += "\n"

        backend = f"Docker container '{self.container_id}'"
        if self._container_name:
            backend += f" ({self._container_name})"
        return CommandResult(
            command=metadata.command,
            args=metadata.args,
            cwd=str(cwd),
            output=output,
            exit_code=process.returncode,
            skipped=False,
            start_time=start_time,
            end_time=datetime.utcnow(),
            backend=backend
        )


    def stop(self):
        """
        Stops the docker container.
        """
        result = Docker.stop(
            self._docker_container_id,
            use_sudo=self._use_sudo,
            cmd_flags=self._cmd_flags,
            pyshell=self._host_pyshell
        )
        if not result.success:
            # This branch can't be easily tested; ignore it for code coverage
            raise RuntimeError( # pragma: no cover
                f"Could not stop container '{self.container_id}'."
            )
