from pathlib import Path
from pyshell.core.command_flags import CommandFlags
from pyshell.core.command_result import CommandResult
from pyshell.core.pyshell import PyShell
from pyshell.doxygen.doxygen_command import DoxygenCommand
from pyshell.modules.module import IModule
from typing import Optional

class Doxygen(IModule):
    """
    Module that simplifies doxygen command execution.
    @ingroup modules
    @ingroup doxygen
    """
    @staticmethod
    def generate_docs(
        doxyfile_path: str | Path,
        cmd_flags: int = CommandFlags.STANDARD,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Returns the results of running `doxygen` on the specified doxyfile.
        @param doxyfile_path The path to the doxyfile to use. Can be a relative
          or absolute path. If the path is relative, it will be resolved
          relative to the script's current working directory.
        @param pyshell PyShell instance to execute the command via.
        @param cmd_flags The flags to set for the command.
        @return The results of running `doxygen` on the doxyfile.
        """
        return DoxygenCommand(doxyfile_path, cmd_flags)(pyshell)
