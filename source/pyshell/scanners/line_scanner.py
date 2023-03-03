from abc import abstractmethod
from pyshell.commands.command_result import CommandResult
from pyshell.scanners.entry import Entry
from pyshell.scanners.scanner import IScanner
from typing import List, Optional

class ILineScanner(IScanner):
    """
    Helper scanner interface that splits command output into lines.
    """
    def scan_for_errors(self, result: CommandResult) -> List[Entry]:
        """
        Scans the command result and generates messages to display to the user.
        @param result The command result to scan.
        @returns A list of scanner entries generated from the output.
        """
        entries: List[Entry] = []
        lines = result.output.splitlines()

        for line_number, line in enumerate(lines):
            entry = self._process_command_line(
                result,
                line,
                lines[line_number + 1:],
                line_number + 1
            )
            if entry is not None:
                entries.append(entry)
        return entries


    @abstractmethod
    def _process_command_line(self,
        result: CommandResult,
        line: str,
        next_lines: List[str],
        line_number: int) -> Optional[Entry]:
        """
        Method invoked for each line in the command output.
        @param result The command result being scanned.
        @param line The line to process.
        @param next_lines The next line(s) in the command output.
        @param line_number The line number of the line.
        @returns An entry for the line if an error is detected, otherwise None.
        """
        raise NotImplementedError()
