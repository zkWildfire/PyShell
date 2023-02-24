from pyshell.core.command_result import CommandResult
from pyshell.core.module import IModule
from pyshell.core.pyshell import PyShell
from pyshell.shell.echo import EchoCommand
from pyshell.shell.ls import LsCommand
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
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Returns the results of running `echo` with the specified message.
        @param message The message to write to stdout.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running `echo`.
        """
        return EchoCommand(message)(pyshell)


    @staticmethod
    def ls(
        target_path: Optional[str] = None,
        pyshell: Optional[PyShell] = None) -> CommandResult:
        """
        Returns the results of running `ls` on the specified path.
        @param target_path The path to list the contents of.
        @param pyshell PyShell instance to execute the command via.
        @return The results of running `ls` on the target path.
        """
        return LsCommand(target_path)(pyshell)
