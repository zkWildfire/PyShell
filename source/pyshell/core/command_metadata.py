from pyshell.core.command_flags import CommandFlags
from pyshell.scanners.scanner import IScanner
from typing import Optional, Sequence

class CommandMetadata:
    """
    Contains all metadata for a single command invocation.
    """
    def __init__(
        self,
        command: str,
        args: Sequence[str],
        flags: int = CommandFlags.STANDARD,
        scanner: Optional[IScanner] = None):
        """
        Initializes the object.
        @param command Command to run.
        @param args Arguments to pass to the command.
        @param flags Flags for the command.
        @param scanner Scanner to use for the command, if any.
        """
        self._command = command
        self._args = args
        self._flags = flags
        self._scanner = scanner


    @property
    def command(self) -> str:
        """
        Returns the command to run.
        """
        return self._command


    @property
    def args(self) -> Sequence[str]:
        """
        Returns the arguments to pass to the command.
        """
        return self._args


    @property
    def full_command(self) -> str:
        """
        Returns the full command to run.
        """
        return " ".join([self._command] + list(self._args))


    @property
    def flags(self) -> int:
        """
        Returns the flags for the command.
        """
        return self._flags


    @property
    def is_standard(self) -> bool:
        """
        Returns True if the command is a standard command.
        """
        return self._flags & CommandFlags.STANDARD != 0


    @property
    def is_inactive(self) -> bool:
        """
        Returns True if the command is inactive.
        """
        return self._flags & CommandFlags.INACTIVE != 0


    @property
    def is_cleanup(self) -> bool:
        """
        Returns True if the command is a cleanup command.
        """
        return self._flags & CommandFlags.CLEANUP != 0


    @property
    def scanner(self) -> Optional[IScanner]:
        """
        Returns the scanner to use for the command, if any.
        """
        return self._scanner
