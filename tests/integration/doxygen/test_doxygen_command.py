# pyright: reportUnusedImport=false
from integration.doxygen.doxygen_fixture import DoxygenFixture, doxy
from pyshell import PyShell, PyShellOptions, AbortOnFailure, KeepGoing, \
    NativeBackend, NullFileLogger
from pyshell.doxygen.doxygen_command import DoxygenCommand
import pytest
from typing import Any

def test_generate_docs(doxy: DoxygenFixture):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        AbortOnFailure(),
        PyShellOptions()
    )

    # Run the doxygen command
    cmd = DoxygenCommand(DoxygenFixture.DOXYFILE_PATH)
    result = cmd(pyshell)
    assert result.success

    # Verify that doxygen files were generated
    assert DoxygenFixture.DOXYGEN_OUTPUT_DIR.exists()
    index_html = DoxygenFixture.DOXYGEN_OUTPUT_DIR.joinpath("html", "index.html")
    assert index_html.exists()
    assert index_html.is_file()


def test_doxypath_does_not_exist():
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        KeepGoing(),
        PyShellOptions()
    )

    # Run the doxygen command
    with pytest.raises(ValueError):
        cmd = DoxygenCommand("foo")
        # This shouldn't be reached
        cmd(pyshell)


def test_doxypath_is_not_a_file(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell(
        NativeBackend(),
        NullFileLogger(),
        KeepGoing(),
        PyShellOptions()
    )

    # Run the doxygen command
    with pytest.raises(ValueError):
        cmd = DoxygenCommand(tmp_path)
        # This shouldn't be reached
        cmd(pyshell)
