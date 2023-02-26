from integration.script_helper import ScriptHelper
from pathlib import Path

class TestSample1:
    # Path to the directory containing the sample scripts
    SAMPLES_DIR = Path(__file__).joinpath(
        "../../../../samples/1-hello-world").absolute().resolve()

    # Script to run
    SCRIPT = "hello_world.py"

    # Log file used by the script when running in single-file mode
    LOG_FILE = "hello_world.log"

    # Logs folder used by the script when running in multi-file mode
    LOGS_DIR = ".logs"

    def test_log_to_console_only(self):
        helper = ScriptHelper(
            self.SAMPLES_DIR,
            self.SCRIPT,
            self.LOG_FILE,
            self.LOGS_DIR
        )

        exit_code, output = helper.run_script()
        assert exit_code == 0
        assert "Hello, world!" in output
        assert "Hello world again!" in output
        assert "Howdy y'all!" in output

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
        assert "Hello, world!" in output
        assert "Hello world again!" in output
        assert "Howdy y'all!" in output

        log_contents = helper.find_log_file(self.LOG_FILE)
        assert log_contents
        assert "Hello, world!" in log_contents
        assert "Hello world again!" in log_contents
        assert "Howdy y'all!" in log_contents


    def test_log_to_multiple_files(self):
        helper = ScriptHelper(
            self.SAMPLES_DIR,
            self.SCRIPT,
            log_file=self.LOG_FILE,
            logs_dir=self.LOGS_DIR
        )

        exit_code, output = helper.run_script(["--log", "multi"])
        assert exit_code == 0
        assert "Hello, world!" in output
        assert "Hello world again!" in output
        assert "Howdy y'all!" in output

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
