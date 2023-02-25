from pyshell import PyShell, PyShellOptions, AbortOnFailure, KeepGoing, \
    NativeBackend, NullFileLogger
from pyshell.shell.rm_command import RmCommand
from typing import Any


def test_rm_file(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AbortOnFailure(),
        PyShellOptions()
    )

    # Create a file to remove
    file_path = tmp_path / "foo.txt"
    file_path.write_text("foo")

    # Run the commands
    cmd = RmCommand(file_path)
    result = cmd(pyshell)
    assert result.success

    # Verify that the file was removed
    assert not file_path.exists()


def test_rm_empty_dir(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AbortOnFailure(),
        PyShellOptions()
    )

    # Create a directory to remove
    dir_path = tmp_path / "foo"
    dir_path.mkdir()

    # Run the commands
    cmd = RmCommand(dir_path)
    result = cmd(pyshell)
    assert result.success

    # Verify that the directory was removed
    assert not dir_path.exists()


def test_rm_non_empty_dir(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AbortOnFailure(),
        PyShellOptions()
    )

    # Create a directory to remove
    dir_path = tmp_path / "foo"
    dir_path.mkdir()

    # Create a file in the directory
    file_path = dir_path / "bar.txt"
    file_path.write_text("foo")

    # Run the commands
    cmd = RmCommand(dir_path)
    result = cmd(pyshell)
    assert result.success

    # Verify that the directory was removed
    assert not dir_path.exists()


def test_rm_non_existent_file(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        KeepGoing(),
        PyShellOptions()
    )

    # Run the commands
    cmd = RmCommand(tmp_path / "foo.txt")
    result = cmd(pyshell)
    assert not result.success


def test_rm_non_existent_dir(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        KeepGoing(),
        PyShellOptions()
    )

    # Run the commands
    cmd = RmCommand(tmp_path / "foo")
    result = cmd(pyshell)
    assert not result.success


def test_force_remove_file(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AbortOnFailure(),
        PyShellOptions()
    )

    # Create a file to remove
    file_path = tmp_path / "foo.txt"
    file_path.write_text("foo")

    # Run the commands
    cmd = RmCommand(file_path, force=True)
    result = cmd(pyshell)
    assert result.success

    # Verify that the file was removed
    assert not file_path.exists()


def test_force_remove_empty_dir(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AbortOnFailure(),
        PyShellOptions()
    )

    # Create a directory to remove
    dir_path = tmp_path / "foo"
    dir_path.mkdir()

    # Run the commands
    cmd = RmCommand(dir_path, force=True)
    result = cmd(pyshell)
    assert result.success

    # Verify that the directory was removed
    assert not dir_path.exists()


def test_force_remove_non_empty_dir(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AbortOnFailure(),
        PyShellOptions()
    )

    # Create a directory to remove
    dir_path = tmp_path / "foo"
    dir_path.mkdir()

    # Create a file in the directory
    file_path = dir_path / "bar.txt"
    file_path.write_text("foo")

    # Run the commands
    cmd = RmCommand(dir_path, force=True)
    result = cmd(pyshell)
    assert result.success

    # Verify that the directory was removed
    assert not dir_path.exists()


def test_force_remove_non_existent_file(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AbortOnFailure(),
        PyShellOptions()
    )

    # Run the commands
    cmd = RmCommand(tmp_path / "foo.txt", force=True)
    result = cmd(pyshell)
    assert result.success


def test_force_remove_non_existent_dir(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AbortOnFailure(),
        PyShellOptions()
    )

    # Run the commands
    cmd = RmCommand(tmp_path / "foo", force=True)
    result = cmd(pyshell)
    assert result.success
