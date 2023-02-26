from abc import ABC, abstractmethod
from pyshell.core.command_result import CommandResult
from pyshell.scanners.entry import Entry
from typing import List

class IScanner(ABC):
    """
    Interface for classes that scan command output for errors.
    Scanners are simplify the process of scanning command output for errors by
      allowing PyShell to output messages at the end of a command's log. These
      messages are the entries returned by the `scan_for_errors()` method, which
      should point out lines that the user will likely need to address to fix
      the error.
    """

    @abstractmethod
    def scan_for_errors(self, result: CommandResult) -> List[Entry]:
        """
        Scans the command result and generates messages to display to the user.
        @param result The command result to scan.
        @returns A list of scanner entries generated from the output.
        """
        raise NotImplementedError()
