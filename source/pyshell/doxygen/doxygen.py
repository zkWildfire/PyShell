from pathlib import Path
from pyshell.core.command import ICommand
from pyshell.core.command_result import CommandResult
from pyshell.core.platform_statics import PlatformStatics
from pyshell.core.pyshell import PyShell
from typing import Optional

class DoxygenCommand(ICommand):
    """
    Defines a command that runs `doxygen`.
    """
    def __init__(self, doxyfile_path: str | Path):
        """
        Initializes the command.
        @param doxyfile_path The path to the doxyfile to use. Can be a relative
          or absolute path. If the path is relative, it will be resolved
          relative to the script's current working directory.
        """
        # Verify that doxygen can be found
        doxygen_exe_path = PlatformStatics.resolve_using_path(
            PlatformStatics.to_executable_name("doxygen")
        )

        # Convert the doxyfile path to an absolute path
        doxyfile_path = Path(doxyfile_path)
        if not doxyfile_path.is_absolute():
            doxyfile_path = Path.cwd() / doxyfile_path

        # Validate the input argument
        if not doxyfile_path.is_file():
            raise ValueError(f"'{doxyfile_path}' is not a file.")

        super().__init__(doxygen_exe_path, doxyfile_path)


    def __call__(self, pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs the command on the specified backend.
        @param pyshell PyShell instance to execute the command via.
        """
        pyshell = self._resolve_pyshell_instance(pyshell)
        return pyshell.run(self.full_command)
