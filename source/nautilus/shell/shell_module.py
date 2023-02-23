from nautilus.core.command_result import CommandResult
from nautilus.core.module import IModule
from nautilus.core.nautilus import Nautilus
from nautilus.shell.echo import EchoCommand
from nautilus.shell.ls import LsCommand
from typing import Optional

class Shell(IModule):
    """
    Module that provides access to shell commands.
    Shell commands that are not supported by the native underlying shell will
      be emulated.
    """
    @staticmethod
    def echo(
        message: Optional[str] = None,
        nautilus: Optional[Nautilus] = None) -> CommandResult:
        """
        Returns the results of running `echo` with the specified message.
        @param message The message to write to stdout.
        @param nautilus Nautilus instance to execute the command via.
        @return The results of running `echo`.
        """
        return EchoCommand(message)(nautilus)


    @staticmethod
    def ls(
        target_path: Optional[str] = None,
        nautilus: Optional[Nautilus] = None) -> CommandResult:
        """
        Returns the results of running `ls` on the specified path.
        @param target_path The path to list the contents of.
        @param nautilus Nautilus instance to execute the command via.
        @return The results of running `ls` on the target path.
        """
        return LsCommand(target_path)(nautilus)
