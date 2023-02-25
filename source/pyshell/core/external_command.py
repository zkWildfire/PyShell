from pathlib import Path
from pyshell.core.command import ICommand
from pyshell.core.command_result import CommandResult
from pyshell.core.pyshell import PyShell
from pyshell.core.platform_statics import PlatformStatics
from typing import Optional, Sequence

class IExternalCommand(ICommand):
    """
    Base class for commands that run external executables.
    """
    def __init__(self,
        name: str | Path,
        args: str | Path | Sequence[str | Path] | None = None,
        locate_executable: bool = True):
        """
        Initializes the command.
        @param name The name of the command being run. This should be the name
          of the executable/command being run but should not include any of
          the arguments.
        @param args The argument(s) to pass to the command.
        @param locate_executable Whether to locate the executable in the PATH.
          If this is true, this constructor will throw if the executable cannot
          be found in the PATH.
        """
        self._name = str(name)
        if isinstance(args, str) or isinstance(args, Path):
            args = [args]
        elif not args:
            args = []
        self._args = [str(a) for a in args]

        # Verify that the executable exists in the PATH if requested
        if locate_executable:
            self._exe_path = PlatformStatics.resolve_using_path(self._name)
        else:
            self._exe_path = self._name
            if not Path(self._exe_path).is_file():
                raise FileNotFoundError(
                    f"Executable '{self._exe_path}' not found"
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
        return pyshell.run(self.full_command, cwd)
