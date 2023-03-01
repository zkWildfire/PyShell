from pathlib import Path
from pyshell.backends.backend import IBackend
from pyshell.core.command_metadata import CommandMetadata
from pyshell.core.command_result import CommandResult
from pyshell.core.pyshell import PyShell
from pyshell.modules.docker import Docker
import subprocess
from typing import IO, Optional

class DockerBackend(IBackend):
    """
    Backend that executes commands in a docker container.
    @ingroup backends
    """
    def __init__(self,
        pyshell: PyShell,
        image: str,
        container_name: Optional[str] = None,
        use_sudo: bool = False):
        """
        Initializes the backend.
        @param pyshell The pyshell instance to use when running docker commands
          to set up the backend. This must be an instance that is configured
          with a backend that will execute commands on the host system, e.g. the
          `NativeBackend` class.
        @param image The docker image to use.
        @param container_name The name of the container to use. If None, a
          random name will be generated.
        @param use_sudo Whether to use `sudo` when running docker commands.
        @throws RuntimeError Thrown if docker is not available or the image
          could not be pulled.
        """
        self._use_sudo = use_sudo
        self._host_pyshell = pyshell

        # Make sure that privileged docker commands can be run
        result = Docker.ps(use_sudo=use_sudo, pyshell=pyshell)
        if not result.success:
            raise RuntimeError(
                "Docker is not available on this system."
            )

        # Pull the image
        result = Docker.pull(image, use_sudo=use_sudo, pyshell=pyshell)
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
            use_sudo=use_sudo,
            pyshell=pyshell
        )
        if not result.success:
            raise RuntimeError(
                f"Could not start container '{container_name}'."
            )

        # Store the docker container's ID
        self._docker_container_id = result.output.strip()
        assert self._docker_container_id
        print(f"Container ID: {self._docker_container_id}")

        # Make sure the container doesn't exit immediately
        # Note that `docker ps` will print the first 12 characters of the
        #   container ID, hence why `[:12]` is used here
        result = Docker.ps(use_sudo=use_sudo, pyshell=pyshell)
        if not self._docker_container_id[:12] in result.output:
            raise RuntimeError(
                f"Container '{container_name}' exited immediately."
            )


    @property
    def docker_container_id(self) -> str:
        """
        The ID of the docker container.
        """
        return self._docker_container_id


    def run(self,
        metadata: CommandMetadata,
        cwd: Path) -> CommandResult:
        """
        Runs the specified command on the backend.
        @param metadata Metadata for the command to run.
        @param cwd The working directory to use for the command. Will always be
          an absolute path.
        @return The output of the command.
        """
        output = ""

        # Invoke the docker exec command directly via subprocess instead of
        #   using `ExecCommand` because `ExecCommand` expects arguments to be
        #   passed to it in specific parameters. Since the backend receives the
        #   command as a single string plus an args array, it's easier and
        #   significantly less error prone to just invoke the docker exec
        #   command directly.
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
            stderr=subprocess.STDOUT,
            cwd=cwd,
            universal_newlines=True
        )

        # Process all output from the process
        assert process.stdout
        while process.poll() is None:
            new_output = DockerBackend._get_output(process.stdout)
            if new_output:
                output += new_output
                print(new_output, end="")

        # Process any remaining output from the process
        while True:
            new_output = DockerBackend._get_output(process.stdout)
            if new_output:
                # These lines are timing dependent; don't track them for coverage
                output += new_output # pragma: no cover
                print(new_output, end="") # pragma: no cover
            else:
                break

        # Add a final newline if the output doesn't end with one
        if not output.endswith("\n"):
            output += "\n"

        return CommandResult(
            command=metadata.command,
            args=metadata.args,
            cwd=str(cwd),
            output=output,
            exit_code=process.returncode,
            skipped=False
        )


    def stop(self):
        """
        Stops the docker container.
        """
        result = Docker.stop(
            self._docker_container_id,
            use_sudo=self._use_sudo,
            pyshell=self._host_pyshell
        )
        if not result.success:
            raise RuntimeError(
                f"Could not stop container '{self._docker_container_id}'."
            )


    @staticmethod
    def _get_output(stream: IO[str]) -> str:
        """
        Gets the current output from the specified stream.
        This method will only return full lines of output. If the stream has
          partial output, this method will return None.
        @param stream The stream to get output from.
        @return The current output from the stream.
        """
        return stream.read()
