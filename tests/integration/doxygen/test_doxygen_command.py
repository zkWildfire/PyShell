# pyright: reportUnusedImport=false
from integration.doxygen.doxygen_fixture import DoxygenFixture, doxy
from pyshell import PyShell, PyShellOptions, AbortOnFailure, NativeBackend, \
    NullFileLogger
from pyshell.doxygen.doxygen_command import DoxygenCommand

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
