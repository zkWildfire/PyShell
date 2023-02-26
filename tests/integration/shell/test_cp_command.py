from pyshell import PyShell, PyShellOptions, AbortOnFailure, AllowAll, \
    KeepGoing, NativeBackend, NullFileLogger
from pyshell.modules.shell import Shell
from pyshell.shell.cp_command import CpCommand
import pytest
from typing import Any


def test_cp_file(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AllowAll(),
        AbortOnFailure(),
        PyShellOptions()
    )

    # Create a file to copy
    src_path = tmp_path / "foo.txt"
    src_path.write_text("foo")

    # Create a destination to copy the file to
    dest_path = tmp_path / "bar.txt"

    # Run the commands
    result = Shell.cp(src_path, dest_path, pyshell)
    assert result.success

    # Verify that the file was copied
    assert dest_path.exists()
    assert dest_path.read_text() == "foo"


def test_cp_empty_dir(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AllowAll(),
        AbortOnFailure(),
        PyShellOptions()
    )

    # Create a directory to copy
    src_path = tmp_path / "foo"
    src_path.mkdir()

    # Create a destination to copy the file to
    dest_path = tmp_path / "bar"

    # Run the commands
    result = Shell.cp(src_path, dest_path, pyshell)
    assert result.success

    # Verify that the directory was copied
    assert dest_path.exists()
    assert dest_path.is_dir()


def test_cp_non_empty_dir(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AllowAll(),
        AbortOnFailure(),
        PyShellOptions()
    )

    # Create a directory to copy
    src_path = tmp_path / "foo"
    src_path.mkdir()
    src_path.joinpath("bar.txt").write_text("bar")

    # Create a destination to copy the file to
    dest_path = tmp_path / "bar"

    # Run the commands
    result = Shell.cp(src_path, dest_path, pyshell)
    assert result.success

    # Verify that the directory was copied
    assert dest_path.exists()
    assert dest_path.is_dir()
    assert dest_path.joinpath("bar.txt").exists()
    assert dest_path.joinpath("bar.txt").read_text() == "bar"


def test_cp_file_to_non_existing_dir(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AllowAll(),
        KeepGoing(),
        PyShellOptions()
    )

    # Create a file to copy
    src_path = tmp_path / "foo.txt"
    src_path.write_text("foo")

    # Create a destination to copy the file to
    dest_path = tmp_path / "bar" / "baz.txt"

    # Run the commands
    result = Shell.cp(src_path, dest_path, pyshell)
    assert not result.success


def test_cp_non_existing_file(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AllowAll(),
        KeepGoing(),
        PyShellOptions()
    )

    # Create a destination to copy the file to
    src_path = tmp_path / "foo.txt"
    dest_path = tmp_path / "bar.txt"

    # Run the commands
    with pytest.raises(ValueError):
        cmd = CpCommand(src_path, dest_path)
        # This shouldn't be reached
        cmd(pyshell)


def test_cp_non_existing_dir(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AllowAll(),
        KeepGoing(),
        PyShellOptions()
    )

    # Create a destination to copy the file to
    src_path = tmp_path / "foo"
    dest_path = tmp_path / "bar"

    # Run the commands
    with pytest.raises(ValueError):
        cmd = CpCommand(src_path, dest_path)
        # This shouldn't be reached
        cmd(pyshell)


def test_cp_file_over_existing_file(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AllowAll(),
        AbortOnFailure(),
        PyShellOptions()
    )

    # Create a file to copy
    src_path = tmp_path / "foo.txt"
    src_path.write_text("foo")

    # Create a destination to copy the file to
    dest_path = tmp_path / "bar.txt"
    dest_path.write_text("bar")

    # Run the commands
    result = Shell.cp(src_path, dest_path, pyshell)
    assert result.success

    # Verify that the file was copied
    assert dest_path.exists()
    assert dest_path.read_text() == "foo"
