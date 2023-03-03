from pathlib import Path
from pyshell.commands.command import ICommand
from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.command_result import CommandResult
from pyshell.core.pyshell import PyShell
from pyshell.core.platform_statics import PlatformStatics
from pyshell.tracing.caller_info import CallerInfo
import sys
from typing import Optional, Sequence

class ExternalCommand(ICommand):
    """
    Base class for commands that run external executables.
    PyShell scripts may use this command to run executables for which PyShell
      does not have native support for. Running a command via this class instead
      of running it via `subprocess` will allow PyShell to log the command and
      handle any errors using the standard PyShell error handling mechanisms.
    @ingroup commands
    """
    def __init__(self,
        name: str | Path,
        args: str | Path | Sequence[str | Path] | None = None,
        locate_executable: bool = True,
        cmd_flags: int = CommandFlags.STANDARD):
        """
        Initializes the command.
        @param name The name of the command being run. This should be the name
          of the executable/command being run but should not include any of
          the arguments.
        @param args The argument(s) to pass to the command.
        @param locate_executable Whether to locate the executable in the PATH.
          If this is true, this constructor will throw if the executable cannot
          be found in the PATH.
        @param flags Flags for the command.
        """
        # Store arguments in a uniform state regardless of input type
        self._name = str(name)
        if isinstance(args, str) or isinstance(args, Path):
            args = [args]
        elif not args:
            args = []
        self._args = [str(a) for a in args]
        self._flags = cmd_flags
        self._origin = CallerInfo.closest_external_frame()
        self._locate_executable = locate_executable


    @property
    def metadata(self) -> CommandMetadata:
        """
        The metadata for the command.
        """
        return CommandMetadata(
            self._name,
            self._args,
            self._flags,
            self.scanner
        )


    @property
    def command_name(self) -> str:
        """
        The name of the command being run.
        This contains the name of the executable/command being run but does not
          include any of the arguments.
        """
        return self._name


    @property
    def args(self) -> Sequence[str]:
        """
        The arguments passed to the command.
        """
        return self._args


    @property
    def full_command(self) -> Sequence[str]:
        """
        The full command being run, including the command name and all arguments.
        """
        return [self.command_name] + self._args


    @property
    def origin(self) -> CallerInfo:
        """
        Gets the location that the command was created at.
        This location will always be the location in the script that uses
          PyShell, not an internal PyShell location.
        """
        return self._origin


    def __call__(self,
        pyshell: Optional[PyShell] = None,
        cwd: str | Path | None = None) -> CommandResult:
        """
        Runs the command on the specified backend.
        @param pyshell PyShell instance to execute the command via.
        @param cwd The current working directory to use for the command. If this
          is not provided, the pyshell instance's cwd will be used.
        """
        pyshell = self._resolve_pyshell_instance(pyshell)

        # Verify that the executable exists in the PATH if requested
        error_msg: Optional[str] = None
        if self._locate_executable:
            try:
                exe_path = PlatformStatics.resolve_using_path(self._name)
            except FileNotFoundError:
                error_msg = f"Executable '{self._name}' not found in PATH.\n"
        else:
            exe_path = self._name
            if not Path(exe_path).is_file():
                error_msg = f"Executable '{exe_path}' not found.\n"

        # If the executable could not be found, print an error message and
        #   return a failed result
        if error_msg:
            error_msg += "Note: Command was declared at " + \
                f"{self.origin.file_path}:{self.origin.line_number}"
            print(error_msg, file=sys.stderr)
            return CommandResult(
                self._name,
                self._args,
                str(cwd) if cwd else str(pyshell.cwd),
                error_msg,
                1,
                False
            )

        # Make sure that all arguments to the command are valid
        error_msg = self._validate_args()
        if error_msg:
            return CommandResult(
                self._name,
                self._args,
                str(cwd) if cwd else str(pyshell.cwd),
                error_msg,
                1,
                False
            )

        return pyshell.run(self.metadata, cwd)


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
        return None
