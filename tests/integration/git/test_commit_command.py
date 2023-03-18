from pathlib import Path
from pyshell import PyShell, KeepGoing
from pyshell.modules.git import Git
from typing import Any

def test_commit_file(tmp_path: Any):
    # Set up a shell in the temporary directory
    pyshell = PyShell()
    pyshell.cd(tmp_path)

    # Create a file
    file = Path(tmp_path, "file.txt")
    file.write_text("foo bar")

    # Run the command
    result = Git.init()
    assert result.success

    result = Git.add(file)
    assert result.success

    result = Git.commit("Initial commit")
    assert result.success


def test_commit_with_no_files_staged(tmp_path: Any):
    # Set up a shell in the temporary directory
    pyshell = PyShell(error_handler=KeepGoing())
    pyshell.cd(tmp_path)

    # Create a file
    file = Path(tmp_path, "file.txt")
    file.write_text("foo bar")

    # Run the command
    result = Git.init()
    assert result.success

    result = Git.commit("Initial commit")
    assert not result.success
