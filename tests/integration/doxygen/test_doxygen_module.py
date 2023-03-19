# pyright: reportUnusedImport=false
from integration.doxygen.doxygen_fixture import DoxygenFixture, doxy
from pyshell import PyShell
from pyshell.modules import Doxygen

def test_generate_docs(doxy: DoxygenFixture):
    # Initialize a PyShell instance for running commands
    pyshell = PyShell()

    # Run the doxygen command
    Doxygen.generate_docs(DoxygenFixture.DOXYFILE_PATH, pyshell=pyshell)

    # Verify that doxygen files were generated
    assert DoxygenFixture.DOXYGEN_OUTPUT_DIR.exists()
    index_html = DoxygenFixture.DOXYGEN_OUTPUT_DIR.joinpath("html", "index.html")
    assert index_html.exists()
    assert index_html.is_file()
