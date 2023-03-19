# pyright: reportUnusedImport=false
from integration.doxygen.doxygen_fixture import DoxygenFixture, doxy
from pyshell import PyShell, KeepGoing
from pyshell.doxygen.doxygen_command import DoxygenCommand
from typing import Any

import os
import pytest

def test_generate_docs(doxy: DoxygenFixture):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell()

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
    pyshell = PyShell(error_handler=KeepGoing())

    # Run the doxygen command
    cmd = DoxygenCommand("foo")
    result = cmd(pyshell)
    assert not result.success

def test_doxypath_is_not_a_file(tmp_path: Any):
    # Initialize a PyShell instance for running commands
    # pyshell = PyShell(error_handler=KeepGoing())

    # Run the doxygen command
    # cmd = DoxygenCommand(tmp_path)
    # result = cmd(pyshell)
    # assert not result.success
    pass
