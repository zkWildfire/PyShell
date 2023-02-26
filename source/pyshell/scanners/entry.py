from pyshell.scanners.severity import ESeverity

class Entry:
    """
    Struct-type class used to store output from a scanner.
    """

    def __init__(self,
        severity: ESeverity,
        cmd_output: str,
        start_line: int,
        end_line: int,
        scanner_output: str):
        """
        Initializes the object.
        @param severity The severity of the scanner entry.
        @param cmd_output The line(s) from the command output that the scanner
          entry is associated with.
        @param start_line The line number in the command output where the
          scanner entry starts.
        @param end_line The line number in the command output where the
          scanner entry ends.
        @param scanner_output The message that the scanner generated for the
          entry.
        """
        assert end_line >= start_line

        self._severity = severity
        self._cmd_output = cmd_output
        self._start_line = start_line
        self._end_line = end_line
        self._scanner_output = scanner_output


    @property
    def severity(self) -> ESeverity:
        """
        Returns the severity of the scanner entry.
        """
        return self._severity


    @property
    def cmd_output(self) -> str:
        """
        Returns the line(s) from the command output that the scanner entry is
        associated with.
        """
        return self._cmd_output


    @property
    def start_line(self) -> int:
        """
        Returns the line number in the command output where the scanner entry
        starts.
        """
        return self._start_line


    @property
    def end_line(self) -> int:
        """
        Returns the line number in the command output where the scanner entry
        ends.
        """
        return self._end_line


    @property
    def scanner_output(self) -> str:
        """
        Returns the message that the scanner generated for the entry.
        """
        return self._scanner_output
