from pathlib import Path
from pyshell import PyShell
from pyshell.modules.git import Git
from typing import Any

def test_status_in_empty_repository(tmp_path: Any):
    # Set up a shell in the temporary directory
    pyshell = PyShell()
    pyshell.cd(tmp_path)

    # Run the command
    result = Git.init()
    assert result.success

    result = Git.status()
    assert result.success
    assert "nothing to commit" in result.output


def test_status_with_untracked_file(tmp_path: Any):
    # Set up a shell in the temporary directory
    pyshell = PyShell()
    pyshell.cd(tmp_path)

    # Create a file
    file = Path(tmp_path, "file.txt")
    file.write_text("foo bar")

    # Run the command
    result = Git.init()
    assert result.success

    result = Git.status()
    assert result.success
    assert "Untracked files:" in result.output
    assert "file.txt" in result.output


def test_status_with_staged_file(tmp_path: Any):
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

    result = Git.status()
    assert result.success
    assert "Changes to be committed:" in result.output
    assert "file.txt" in result.output


def test_status_with_modified_file(tmp_path: Any):
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

    file.write_text("foo bar baz")

    result = Git.status()
    assert result.success
    assert "Changes not staged for commit:" in result.output
    assert "file.txt" in result.output


def test_status_with_porcelain_format(tmp_path: Any):
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

    file.write_text("foo bar baz")

    result = Git.status(porcelain=True)
    assert result.success
    assert "file.txt" in result.output
    assert "M" in result.output
    assert "A" in result.output
