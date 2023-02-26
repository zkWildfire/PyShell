from pathlib import Path
import shutil
import pytest

class DoxygenFixture:
    """
    Fixture that handles cleanup for doxygen tests.
    """

    # Path to the repo's doxyfile
    DOXYFILE_PATH = Path(__file__).parent.joinpath("doxyfile")

    # Working directory that each command must use
    # This is the directory that relative paths in the doxyfile are relative to
    CWD = Path(__file__).parent.joinpath("../../..")

    # Path that doxygen will write its generated files to
    DOXYGEN_OUTPUT_DIR = CWD.joinpath(".docs")


    def clean(self):
        """
        Removes all files and directories generated by this test.
        """
        if DoxygenFixture.DOXYGEN_OUTPUT_DIR.exists():
            shutil.rmtree(DoxygenFixture.DOXYGEN_OUTPUT_DIR)


@pytest.fixture()
def doxy():
    fixture = DoxygenFixture()

    # Make sure all previously generated files are removed before running the
    #   test
    fixture.clean()
    yield fixture

    # Doxygen produces a large number of files. Clear them out to avoid leaving
    #   them behind after the test
    fixture.clean()
