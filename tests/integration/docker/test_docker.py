import os
from pyshell import PyShell, KeepGoing
from pyshell.modules.docker import Docker

class TestDocker:
    # If this is being run in a dev container or on a CI server, `use_sudo`
    #   must be set to True
    use_sudo = os.getenv("DEV_CONTAINER") == "1"

    def test_run_container(self):
        # Initialize a PyShell instance for running commands
        pyshell = PyShell()

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
        pyshell = PyShell()

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
