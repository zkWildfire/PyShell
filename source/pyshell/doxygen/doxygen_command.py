from pathlib import Path
from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.external_command import ExternalCommand
from pyshell.core.platform_statics import PlatformStatics
from pyshell.doxygen.doxygen_scanner import DoxygenScanner
from pyshell.scanners.scanner import IScanner
from typing import Optional

class DoxygenCommand(ExternalCommand):
    """
    Defines a command that runs `doxygen`.
    @ingroup commands
    @ingroup doxygen
    """
    def __init__(self,
        doxyfile_path: str | Path,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param doxyfile_path The path to the doxyfile to use. Can be a relative
          or absolute path. If the path is relative, it will be resolved
          relative to the script's current working directory.
        @param cmd_flags The flags to set for the command.
        """
        # Verify that doxygen can be found
        doxygen_exe_path = PlatformStatics.resolve_using_path(
            PlatformStatics.to_executable_name("doxygen")
        )

        # Convert the doxyfile path to an absolute path
        doxyfile_path = Path(doxyfile_path)
        if not doxyfile_path.is_absolute():
            doxyfile_path = Path.cwd() / doxyfile_path
        self._doxyfile_path = doxyfile_path

        super().__init__(
            doxygen_exe_path,
            doxyfile_path,
            cmd_flags=cmd_flags
        )


    @property
    def scanner(self) -> Optional[IScanner]:
        """
        The scanner to use for the command.
        @return The scanner to use for the command, or None if no scanner should
          be used.
        """
        return DoxygenScanner()


    def _validate_args(self) -> Optional[str]:
        """
        Validates the arguments for the command.
        This method should be overridden by subclasses to validate the arguments
          for the command. If the arguments are valid, this method should
          return None. If the arguments are invalid, this method should return
          a string describing the error.
        @returns None if the arguments are valid, or a string describing the
          error if the arguments are invalid.
        """
        if not self._doxyfile_path.is_file():
            return f"'{self._doxyfile_path}' is not a file."

        return None
