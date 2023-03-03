import os
from pathlib import Path
from pyshell.backends.docker_backend import DockerBackend
from pyshell.core.pyshell import PyShell
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.error.keep_going import KeepGoing
from pyshell.logging.console_command_logger import ConsoleCommandLogger
from pyshell.logging.split_command_logger import SplitCommandLogger
import pytest


class TestDocker:
    # If this is being run in a dev container or on a CI server, `use_sudo`
    #   must be set to True
    use_sudo = os.getenv("DEV_CONTAINER") == "1"

    def test_pull_non_existent_image(self):
        """
        Simulates the case where the docker image to pull does not exist.
        """
        host_pyshell = PyShell(error_handler=KeepGoing())
        with pytest.raises(RuntimeError) as e:
            DockerBackend(host_pyshell, "foo:bar", use_sudo=self.use_sudo)
        assert "Could not pull image" in str(e)


    def test_container_that_fails_to_start(self):
        host_pyshell = PyShell(error_handler=KeepGoing())

        # This container should start without issue since the port is not being
        #   used yet
        success_backend = DockerBackend(
            host_pyshell,
            "ubuntu:jammy",
            ports="1234:8080",
            use_sudo=self.use_sudo
        )

        # Silence the unused variable warning
        assert success_backend

        # This container should fail to start since the port is already in use
        with pytest.raises(RuntimeError) as e:
            failed_backend = DockerBackend(
                host_pyshell,
                "ubuntu:jammy",
                ports=["1234:8080"],
                use_sudo=self.use_sudo
            )

            # Silence the unused variable warning
            # Note that this line should not be reached
            assert failed_backend

        success_backend.stop()
        assert "Could not start container" in str(e)


    def test_start_container_that_exits_immediately(self):
        """
        Simulates the case where the docker container exits immediately.
        """
        host_pyshell = PyShell(error_handler=KeepGoing())
        with pytest.raises(RuntimeError) as e:
            DockerBackend(host_pyshell, "hello-world", use_sudo=self.use_sudo)
        assert "exited immediately" in str(e)


    def test_container_id(self):
        host_pyshell = PyShell()
        backend = DockerBackend(
            host_pyshell,
            "ubuntu:jammy",
            use_sudo=self.use_sudo
        )
        backend.stop()
        assert backend.container_id


    def test_named_container_that_fails_to_start(self):
        host_pyshell = PyShell(error_handler=KeepGoing())

        # This container should start without issue since the port is not being
        #   used yet
        success_backend = DockerBackend(
            host_pyshell,
            "ubuntu:jammy",
            container_name="test_container",
            ports="1234:8080",
            use_sudo=self.use_sudo
        )

        # Silence the unused variable warning
        assert success_backend

        # This container should fail to start since the port is already in use
        failed_container_name = "test_container2"
        with pytest.raises(RuntimeError) as e:
            failed_backend = DockerBackend(
                host_pyshell,
                "ubuntu:jammy",
                container_name=failed_container_name,
                ports=["1234:8080"],
                use_sudo=self.use_sudo
            )

            # Silence the unused variable warning
            # Note that this line should not be reached
            assert failed_backend

        success_backend.stop()
        assert "Could not start container" in str(e)
        assert failed_container_name in str(e)


    def test_named_container_that_exits_immediately(self):
        """
        Simulates the case where the docker container exits immediately.
        """
        host_pyshell = PyShell(error_handler=KeepGoing())
        container_name = "test_container"
        with pytest.raises(RuntimeError) as e:
            DockerBackend(
                host_pyshell,
                "hello-world",
                container_name=container_name,
                use_sudo=self.use_sudo
            )
        assert "exited immediately" in str(e)
        assert container_name in str(e)


    def test_run_with_split_streams(self):
        # Set up the backend
        host_pyshell = PyShell()
        backend = DockerBackend(
            host_pyshell,
            "ubuntu:jammy",
            use_sudo=self.use_sudo
        )

        # Set up the command to run
        msg = "foo"
        metadata = CommandMetadata("echo", [msg])
        cwd = Path("/tmp")

        # Set up the command logger
        stdout_logger = ConsoleCommandLogger(metadata, cwd)
        stderr_logger = ConsoleCommandLogger(metadata, cwd)
        split_logger = SplitCommandLogger(stdout_logger, stderr_logger)

        # Run the test
        result = backend.run(metadata, cwd, split_logger)
        backend.stop()

        assert result.success
        assert msg in stdout_logger.output
        assert not stderr_logger.output.strip()


    def test_run_with_merged_streams(self):
        # Set up the backend
        host_pyshell = PyShell()
        backend = DockerBackend(
            host_pyshell,
            "ubuntu:jammy",
            use_sudo=self.use_sudo
        )

        # Set up the command to run
        msg = "foo"
        metadata = CommandMetadata("bash", ["-c", f"echo {msg} >&2"])
        cwd = Path("/tmp")

        # Set up the command logger
        stdout_logger = ConsoleCommandLogger(metadata, cwd)

        # Run the test
        result = backend.run(metadata, cwd, stdout_logger)
        backend.stop()

        assert result.success
        assert msg in stdout_logger.output
