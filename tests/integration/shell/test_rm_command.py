from pyshell import PyShell, PyShellOptions, AbortOnFailure, KeepGoing, \
    NativeBackend, NullFileLogger
from pyshell.modules.shell import Shell
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
    result = Shell.rm(file_path, pyshell=pyshell)
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
    result = Shell.rm(dir_path, pyshell=pyshell)
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
    result = Shell.rm(dir_path, pyshell=pyshell)
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
    result = Shell.rm(tmp_path / "foo.txt", pyshell=pyshell)
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
    result = Shell.rm(tmp_path / "foo", pyshell=pyshell)
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
    result = Shell.rm(file_path, force=True, pyshell=pyshell)
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
    result = Shell.rm(dir_path, force=True, pyshell=pyshell)
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
    result = Shell.rm(dir_path, force=True, pyshell=pyshell)
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
    result = Shell.rm(tmp_path / "foo.txt", force=True, pyshell=pyshell)
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
    result = Shell.rm(tmp_path / "foo", force=True, pyshell=pyshell)
    assert result.success
