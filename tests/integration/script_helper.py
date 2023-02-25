from pathlib import Path
import shutil
import subprocess
from typing import Optional, Sequence

class ScriptHelper:
    """
    Defines helper methods for managing a script invoked by test cases.
    """
    def __init__(self,
        script_dir: str | Path,
        script_name: str,
        log_file: str | Path | None = None,
        logs_dir: str | Path | None = None,
        clean_logs: bool = True):
        """
        Initializes the helper.
        @param script_dir Path to the directory containing the pyshell script
          that the test will run. Can be a relative or absolute path. If the
          path is a relative path, it will be interpreted relative to the
          current working directory.
        @param script_name Name of the pyshell script to run. This should be a
          file name only. The script must be located in the script directory,
          not any subdirectory.
        @param logs_path Path to the file that pyshell will log to. If this is
          a relative path, it will be interpreted relative to the script
          directory.
        @param logs_dir Name of the logs directory used by the pyshell script.
          This is expected to be a path relative to the script directory.
        @param clean_logs Whether to delete any existing log files before
          running the test.
        """
        # Convert paths into absolute paths
        script_dir = Path(script_dir)
        if not script_dir.is_absolute():
            script_dir = Path.cwd() / script_dir

        log_file = Path(log_file) if log_file else None
        if log_file and not log_file.is_absolute():
            log_file = script_dir / log_file

        logs_dir = Path(logs_dir) if logs_dir else None
        if logs_dir and not logs_dir.is_absolute():
            logs_dir = script_dir / logs_dir

        # Make sure the path is to a folder that's a PyMake project
        script_path = script_dir / script_name
        if not (script_path).exists():
            raise ValueError("Failed to find the sample script.")

        # Each of these member variables will be an absolute path
        self._script_dir = script_dir
        self._script_path = script_path
        self._log_path = log_file
        self._logs_dir = logs_dir

        if clean_logs:
            self.clean_logs()


    def clean_logs(self):
        """
        Delete all log files.
        """
        if self._log_path and self._log_path.exists():
            self._log_path.unlink()

        if self._logs_dir and self._logs_dir.exists():
            shutil.rmtree(self._logs_dir)


    def find_log_file(self,
        file_name: str,
        output_path: Optional[str] = None) -> Optional[str]:
        """
        Finds a log file and returns its contents.
        @param file_name Name of the file to find.
        @param output_path Path to the directory where the file should be found.
            Must be a path relative to the script directory if provided. Can be
            a path to a file or folder. If the path is to a folder, only that
            folder will be searched for a file with the target name. If not
            provided, the entire script directory will be searched.
        @return The contents of the file if it was found, or None if it wasn't.
        """
        # Determine which directory should be searched
        search_dir = self._script_dir
        if output_path:
            search_dir /= output_path

        # `search_dir` can be a path to a file or folder. If it's a path to a
        #   folder, only search that folder. If the path is to a file, simply
        #   check if a file exists at that path.
        if not search_dir.is_dir():
            if search_dir.exists():
                return search_dir.read_text()
            else:
                return None

        # Search the directory for the file
        for f in search_dir.rglob(file_name):
            return f.read_text()
        return None


    def run_script(self, args: Sequence[str] = []) -> int:
        """
        Runs the pyshell script.
        @param args Arguments to pass to the script.
        @returns The exit code from the script.
        """
        return subprocess.run(
            ["python3", str(self._script_path), *args],
            cwd=self._script_dir
        ).returncode
