from pathlib import Path
from pyshell.core.command_result import CommandResult
from pyshell.core.module import IModule
from pyshell.core.pyshell import PyShell
from pyshell.moxygen.moxygen import MoxygenCommand
from typing import Optional

class Moxygen(IModule):
    """
    Module that simplifies moxygen command execution.
    """
    @staticmethod
    def generate_docs(
        doxygen_xml_path: str | Path,
        output_file: str | Path,
        separate_groups: bool = False,
        separate_classes: bool = False,
        separate_pages: bool = False,
        language: Optional[str] = None,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Returns the results of running `moxygen`.
        @param doxygen_xml_dir Path to the folder where doxygen generated its
          XML output. Can be a relative or absolute path. If the path is a
          relative path, it will be resolved relative to the script's current
          working directory.
        @param output_file Value to pass to moxygen as the --output argument.
          Note that if one of the `separate_*` arguments is True, you must
          include "%s" in this string.
        @param separate_groups If True, moxygen will generate separate
          documentation pages for each doxygen group.
        @param separate_classes If True, moxygen will generate separate
          documentation pages for each doxygen class.
        @param separate_pages If True, moxygen will generate separate
          documentation pages for each doxygen page.
        @param language Passed to moxygen as the --language argument. If None,
          the --language argument will not be passed to moxygen.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running `moxygen` with the specified arguments.
        """
        return MoxygenCommand(
            doxygen_xml_path,
            output_file,
            separate_groups,
            separate_classes,
            separate_pages,
            language
        )(pyshell)
