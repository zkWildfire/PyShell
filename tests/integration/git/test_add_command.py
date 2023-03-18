from pathlib import Path
from pyshell import PyShell, KeepGoing
from pyshell.modules.git import Git
from typing import Any

def test_add_file(tmp_path: Any):
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


def test_add_nonexistent_file(tmp_path: Any):
    # Set up a shell in the temporary directory
    pyshell = PyShell(error_handler=KeepGoing())
    pyshell.cd(tmp_path)

    # Create a file
    file = Path(tmp_path, "file.txt")

    # Run the command
    result = Git.init()
    assert result.success

    result = Git.add(file)
    assert not result.success


def test_add_all_untracked_files(tmp_path: Any):
    # Set up a shell in the temporary directory
    pyshell = PyShell()
    pyshell.cd(tmp_path)

    # Create a file
    file = Path(tmp_path, "file.txt")
    file.write_text("foo bar")

    # Run the command
    result = Git.init()
    assert result.success

    result = Git.add(untracked_only=True)
    assert result.success
