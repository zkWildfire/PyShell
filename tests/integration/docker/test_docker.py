import os
from pyshell import PyShell, KeepGoing
from pyshell.modules.docker import Docker
from typing import Any

class TestDocker:
    # If this is being run in a dev container or on a CI server, `use_sudo`
    #   must be set to True
    use_sudo = os.getenv("DEV_CONTAINER") == "1"

    def test_run_container(self):
        # Initialize a PyShell instance for running commands
        pyshell = PyShell(error_handler=KeepGoing())

        # Start the container, then clean it up before checking test results
        # This is done to ensure that the container is always fully cleaned up
        #   before the test ends
        container_name = "hello-world-test"
        run_result = Docker.run(
            "hello-world",
            container_name=container_name,
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )
        ps_result = Docker.ps(
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )
        ps_a_result = Docker.ps(
            show_all=True,
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )
        rm_result = Docker.rm(
            container_name,
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )

        # Verify the run command
        assert run_result.success
        assert "Hello from Docker!" in run_result.output

        # Verify the ps command
        assert ps_result.success
        assert container_name not in ps_result.output

        # Verify the ps -a command
        assert ps_a_result.success
        assert container_name in ps_a_result.output

        # Verify the rm command
        assert rm_result.success


    def test_run_nonexistent_image(self):
        # Initialize a PyShell instance for running commands
        pyshell = PyShell(error_handler=KeepGoing())

        # Run the run command
        result = Docker.run(
            "nonexistent-image",
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )
        assert not result.success


    def test_run_container_and_remove_when_complete(self):
        # Initialize a PyShell instance for running commands
        pyshell = PyShell(error_handler=KeepGoing())

        # Run all docker commands before checking test results
        # This is done to ensure that even if the run command doesn't remove the
        #   container, the container will still be cleaned up before the test
        #   ends
        container_name = "hello-world-test"
        run_result = Docker.run(
            "hello-world",
            container_name=container_name,
            remove_after=True,
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )
        ps_result = Docker.ps(
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )
        ps_a_result = Docker.ps(
            show_all=True,
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )
        rm_result = Docker.rm(
            container_name,
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )


        # Verify the run command
        assert run_result.success
        assert "Hello from Docker!" in run_result.output

        # Verify the ps command
        assert ps_result.success
        assert container_name not in ps_result.output

        # Verify the ps -a command
        assert ps_a_result.success
        assert container_name not in ps_a_result.output

        # Verify that the container has been removed
        assert not rm_result.success


    def test_pass_environment_variables(self):
        # Initialize a PyShell instance for running commands
        pyshell = PyShell(error_handler=KeepGoing())

        # Run the run command
        container_name = "ubuntu-test"
        test_value = "test_value"
        result = Docker.run(
            "ubuntu:jammy",
            "bash",
            ["-c", "echo $TEST_VAR"],
            container_name=container_name,
            env={"TEST_VAR": test_value},
            remove_after=True,
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )
        assert result.success

        # Verify that the output is correct
        assert test_value in result.output


    def test_stop_then_start_container(self):
        # Initialize a PyShell instance for running commands
        pyshell = PyShell(error_handler=KeepGoing())

        # Start the container
        container_name = "ubuntu-test"
        run_result = Docker.run(
            "ubuntu:jammy",
            "bash",
            interactive=True,
            tty=True,
            detach=True,
            container_name=container_name,
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )

        # Stop the container
        stop_result = Docker.stop(
            container_name,
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )

        # Start the container again
        start_result = Docker.start(
            container_name,
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )

        # Execute a command in the container
        exec_result = Docker.exec(
            container_name,
            "bash",
            ["-c", "echo foo"],
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )

        # Clean up the container
        re_stop_result = Docker.stop(
            container_name,
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )
        rm_result = Docker.rm(
            container_name,
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )

        # Validate results
        assert run_result.success
        assert stop_result.success
        assert start_result.success
        assert exec_result.success
        assert re_stop_result.success
        assert rm_result.success
        assert "foo" in exec_result.output


    def test_force_remove_container(self):
        # Initialize a PyShell instance for running commands
        pyshell = PyShell(error_handler=KeepGoing())

        # Start the container
        container_name = "ubuntu-test"
        run_result = Docker.run(
            "ubuntu:jammy",
            "bash",
            interactive=True,
            tty=True,
            detach=True,
            container_name=container_name,
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )

        # Force remove the container
        rm_result = Docker.rm(
            container_name,
            force=True,
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )

        # Validate results
        assert run_result.success
        assert rm_result.success


    def test_run_container_with_volume(self, tmp_path: Any):
        # Initialize a PyShell instance for running commands
        pyshell = PyShell(error_handler=KeepGoing())

        # Since the standard environment for PyShell development (and its CI/CD
        #   pipeline) is a docker container, this test needs to be a little
        #   hacky to ensure that a file created by the test script, running in
        #   a docker container, can be mounted into another docker container
        #   started by this test script (which is also running in a docker
        #   container, if that hasn't been mentioned before).
        # Here's how this works:
        #   1. A dummy container is started which has a folder from /tmp
        #      mounted into it. This folder is `not` from this container, but
        #      will instead be from the host machine.
        #   2. The dummy container generates a file in the mounted folder
        #      using a command from this script. This ensures that the file
        #      contents are known to this script.
        #   3. The dummy container is stopped and removed.
        #   4. A new container is started which has the same folder mounted
        #      into it. Once again, this is a folder from the host system, *not*
        #      this container.
        #   5. This second container reads from and outputs the contents of
        #      the file created in step 2 to stdout, where it can be captured
        #      by this script.

        # Start the dummy container
        # This `docker run` command implements steps 1-3
        file_contents = "foo bar baz"
        run_result = Docker.run(
            "ubuntu:jammy",
            "bash",
            ["-c", f"echo '{file_contents}' > /tmp/foo/bar"],
            container_name="ubuntu-test-1",
            interactive=True,
            tty=True,
            detach=True,
            volumes=[f"{tmp_path}:/tmp/foo:rw"],
            remove_after=True,
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )

        # Verify that the dummy container ran successfully
        # Since the container is started with `remove_after=True`, there's no
        #   danger of leaving a container behind after the test is complete even
        #   if this assert fails.
        assert run_result.success

        # Create the new container
        # This `docker run` command implements steps 4
        run_result = Docker.run(
            "ubuntu:jammy",
            "bash",
            container_name="ubuntu-test-2",
            interactive=True,
            tty=True,
            detach=True,
            volumes=[f"{tmp_path}:/tmp/foo:ro"],
            remove_after=True,
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )

        # Attempt to read the file created in the dummy container
        # Note that this must be done as part of a separate command since
        #   `docker run` will only print the ID of the container it creates and
        #   not any of the output from the container's stdout
        read_result = Docker.exec(
            "ubuntu-test-2",
            "bash",
            ["-c", "cat /tmp/foo/bar"],
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )
        stop_result = Docker.stop(
            "ubuntu-test-2",
            pyshell=pyshell,
            use_sudo=self.use_sudo
        )

        # Validate the results
        assert run_result.success
        assert read_result.success
        assert stop_result.success
        assert file_contents in read_result.output