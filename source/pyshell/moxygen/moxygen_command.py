import os
from pathlib import Path
from pyshell.core.command import ICommand
from pyshell.core.command_result import CommandResult
from pyshell.core.platform_statics import PlatformStatics
from pyshell.core.pyshell import PyShell
from typing import List, Optional

class MoxygenCommand(ICommand):
    """
    Defines a command that runs `moxygen`.
    """
    def __init__(self,
        doxygen_xml_dir: str | Path,
        output_file: str | Path,
        separate_groups: bool = False,
        separate_classes: bool = False,
        separate_pages: bool = False,
        language: Optional[str] = None):
        """
        Initializes the command.
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
        """
        # Store the output path so that parent directories can be created when
        #   the command is run
        self._output_path = Path(output_file).parent.resolve()

        # Verify that moxygen can be found
        moxygen_exe_path = PlatformStatics.resolve_using_path(
            PlatformStatics.to_executable_name("moxygen")
        )

        # Convert the doxygen xml path to an absolute path
        doxygen_xml_dir = Path(doxygen_xml_dir)
        if not doxygen_xml_dir.is_absolute():
            doxygen_xml_dir = Path.cwd() / doxygen_xml_dir

        # Validate the input argument
        if not doxygen_xml_dir.is_dir():
            raise ValueError(f"'{doxygen_xml_dir}' is not a directory.")
        if not doxygen_xml_dir.joinpath("index.xml").is_file():
            raise ValueError(f"'{doxygen_xml_dir}' does not contain 'index.xml'.")

        # Determine what flags should be passed to moxygen
        flags: List[str] = ["--output", str(output_file)]
        if separate_groups:
            flags.append("--groups")
        if separate_classes:
            flags.append("--classes")
        if separate_pages:
            flags.append("--pages")
        if language is not None:
            flags.extend(["--language", language])

        super().__init__(moxygen_exe_path, flags + [doxygen_xml_dir])


    def __call__(self, pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs the command on the specified backend.
        @param pyshell PyShell instance to execute the command via.
        """
        pyshell = self._resolve_pyshell_instance(pyshell)

        # If the output path doesn't exist, Moxygen will fail
        os.makedirs(self._output_path, exist_ok=True)

        return pyshell.run(self.full_command)
