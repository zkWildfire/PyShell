from pathlib import Path
from pyshell.core.command_result import CommandResult
from pyshell.core.external_command import ExternalCommand
from pyshell.core.module import IModule
from pyshell.core.pyshell import PyShell
from pyshell.shell.cp_command import CpCommand
from pyshell.shell.echo_command import EchoCommand
from pyshell.shell.ls_command import LsCommand
from pyshell.shell.rm_command import RmCommand
from typing import Optional, Sequence

class Shell(IModule):
    """
    Module that provides access to shell commands.
    Shell commands that are not supported by the native underlying shell will
      be emulated.
    @ingroup modules
    @ingroup shell
    """
    @staticmethod
    def cp(
        src: str | Path,
        dest: str | Path,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `cp` on the specified source and destination.
        @param src File or directory to copy. Can be a relative or absolute
          path. If the path is relative, it will be resolved relative to the
          script's current working directory.
        @param dest Destination to copy the file or directory to. Can be a
          relative or absolute path. If the path is relative, it will be
          resolved relative to the script's current working directory.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running `cp` on the source and destination.
        """
        return CpCommand(src, dest)(pyshell)


    @staticmethod
    def echo(
        message: Optional[str] = None,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `echo` with the specified message.
        @param message The message to write to stdout.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running `echo`.
        """
        return EchoCommand(message)(pyshell)


    @staticmethod
    def run(
        command: str,
        args: str | Path | Sequence[str | Path] | None = None,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs an arbitrary command via PyShell.
        @param command The command to run.
        @param args Arguments to pass to the command.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running the command.
        """
        return ExternalCommand(command, args)(pyshell)


    @staticmethod
    def ls(
        target_path: str | Path | None = None,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `ls` on the specified path.
        @param target_path The path to list the contents of.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running `ls` on the target path.
        """
        return LsCommand(target_path)(pyshell)


    @staticmethod
    def rm(
        target_path: str | Path,
        force: bool = False,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Runs `rm` on the specified path.
        @param target_path The path to remove.
        @param force If True, the -f flag will be passed to `rm`.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running `rm` on the target path.
        """
        return RmCommand(target_path, force)(pyshell)
