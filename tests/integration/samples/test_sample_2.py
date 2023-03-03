from integration.script_helper import ScriptHelper
from pathlib import Path

class TestSample2:
    # Path to the directory containing the sample scripts
    SAMPLES_DIR = Path(__file__).joinpath(
        "../../../../samples/2-docker-hello-world").absolute().resolve()

    # Script to run
    SCRIPT = "docker_hello_world.py"

    # Log file used by the script when running in single-file mode
    LOG_FILE = "hello_world.log"

    # Logs folder used by the script when running in multi-file mode
    LOGS_DIR = ".logs"

    # Base number of times a message is expected to appear.
    # The docker hello world script prints each message 3 times - once to the
    #   host before the docker backend is used, once via the docker backend,
    #   and again to the host after the docker backend is shut down. However,
    #   for some tests, this value must be modified to account for extra
    #   instances of the target string appearing as a result of the command
    #   being printed as part of a command header/footer.
    BASE_MESSAGE_COUNT = 3

    # Number of times a message will appear if command headers are used
    HEADER_MESSAGE_COUNT = BASE_MESSAGE_COUNT * 2

    # Number of times a message will appear if command footers are used
    # Note that this is a higher number than the header count because the
    #   sample script only supports enabling headers and footers, not footers
    #   alone. This differs from headers, which may be enabled without footers.
    FOOTER_MESSAGE_COUNT = BASE_MESSAGE_COUNT * 3

    def test_log_to_console_only(self):
        helper = ScriptHelper(
            self.SAMPLES_DIR,
            self.SCRIPT,
            self.LOG_FILE,
            self.LOGS_DIR
        )

        exit_code, output = helper.run_script()
        assert exit_code == 0
        assert output.count("Hello, world!") == self.BASE_MESSAGE_COUNT
        assert output.count("Hello world again!") == self.BASE_MESSAGE_COUNT
        assert output.count("Howdy y'all!") == self.BASE_MESSAGE_COUNT

        log_contents = helper.find_log_file(self.LOG_FILE)
        assert not log_contents
        assert helper.logs_dir
        assert not helper.logs_dir.exists()


    def test_log_to_single_file(self):
        helper = ScriptHelper(
            self.SAMPLES_DIR,
            self.SCRIPT,
            log_file=self.LOG_FILE,
            logs_dir=self.LOGS_DIR
        )

        exit_code, output = helper.run_script(["--log", "single"])
        assert exit_code == 0
        assert output.count("Hello, world!") == self.BASE_MESSAGE_COUNT
        assert output.count("Hello world again!") == self.BASE_MESSAGE_COUNT
        assert output.count("Howdy y'all!") == self.BASE_MESSAGE_COUNT

        log_contents = helper.find_log_file(self.LOG_FILE)
        assert log_contents
        assert log_contents.count("Hello, world!") == self.BASE_MESSAGE_COUNT
        assert log_contents.count("Hello world again!") == self.BASE_MESSAGE_COUNT
        assert log_contents.count("Howdy y'all!") == self.BASE_MESSAGE_COUNT


    def test_log_to_multiple_files(self):
        helper = ScriptHelper(
            self.SAMPLES_DIR,
            self.SCRIPT,
            log_file=self.LOG_FILE,
            logs_dir=self.LOGS_DIR
        )

        exit_code, output = helper.run_script(["--log", "multi"])
        assert exit_code == 0
        assert output.count("Hello, world!") == self.BASE_MESSAGE_COUNT
        assert output.count("Hello world again!") == self.BASE_MESSAGE_COUNT
        assert output.count("Howdy y'all!") == self.BASE_MESSAGE_COUNT

        # Check each of the log files that should have been generated
        # Note that this check is not comprehensive since it does not check for
        #   the command string in the log file and does not verify that each
        #   commands' log file contains output from only the command that was
        #   run. This is unlikely to be an issue since the unit test suite
        #   should be fairly comprehensive but such checks could be added in
        #   the future if needed.
        log_files = [
            ("1-echo.log", "Hello, world!"),
            ("2-echo.log", "Hello world again!"),
            ("3-echo.log", "Howdy y'all!")
        ]
        for log_file, contents in log_files:
            log_contents = helper.find_log_file(log_file, self.LOGS_DIR)
            assert log_contents
            assert contents in log_contents


    def test_log_cmd_headers(self):
        helper = ScriptHelper(
            self.SAMPLES_DIR,
            self.SCRIPT,
            log_file=self.LOG_FILE,
            logs_dir=self.LOGS_DIR
        )

        exit_code, output = helper.run_script(["--log", "single", "-v"])
        assert exit_code == 0
        assert output.count("Hello, world!") == self.HEADER_MESSAGE_COUNT
        assert output.count("Hello world again!") == self.HEADER_MESSAGE_COUNT
        assert output.count("Howdy y'all!") == self.HEADER_MESSAGE_COUNT

        log_contents = helper.find_log_file(self.LOG_FILE)
        assert log_contents
        assert log_contents.count("Hello, world!") == self.HEADER_MESSAGE_COUNT
        assert log_contents.count("Hello world again!") == self.HEADER_MESSAGE_COUNT
        assert log_contents.count("Howdy y'all!") == self.HEADER_MESSAGE_COUNT
        assert "Running command" in log_contents


    def test_log_cmd_footers(self):
        helper = ScriptHelper(
            self.SAMPLES_DIR,
            self.SCRIPT,
            log_file=self.LOG_FILE,
            logs_dir=self.LOGS_DIR
        )

        exit_code, output = helper.run_script(["--log", "single", "-vv"])
        assert exit_code == 0
        assert output.count("Hello, world!") == self.FOOTER_MESSAGE_COUNT
        assert output.count("Hello world again!") == self.FOOTER_MESSAGE_COUNT
        assert output.count("Howdy y'all!") == self.FOOTER_MESSAGE_COUNT

        log_contents = helper.find_log_file(self.LOG_FILE)
        assert log_contents
        assert log_contents.count("Hello, world!") == self.FOOTER_MESSAGE_COUNT
        assert log_contents.count("Hello world again!") == self.FOOTER_MESSAGE_COUNT
        assert log_contents.count("Howdy y'all!") == self.FOOTER_MESSAGE_COUNT
        assert "Executed command" in log_contents
