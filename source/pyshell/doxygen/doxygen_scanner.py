from pyshell.core.command_result import CommandResult
from pyshell.scanners.entry import Entry
from pyshell.scanners.line_scanner import ILineScanner
from pyshell.scanners.severity import ESeverity
from typing import List, Optional
import re

class DoxygenScanner(ILineScanner):
    """
    Scanner that detects doxygen errors.
    """
    def __init__(self):
        """
        Initializes the scanner.
        """
        # Regex for detecting missing parameter documentation.
        # This regex matches lines like the following (extra line breaks added
        #   for readability):
        # ```
        # /workspaces/PyShell/source/pyshell/doxygen/doxygen_scanner.py:20:
        #   error: The following parameter of
        #   pyshell.doxygen.doxygen_scanner.DoxygenScanner._process_command_line(
        #   self, CommandResult result, str line, int line_number) is not
        #   documented:
        # parameter 'result' (warning treated as error, aborting now)
        # ```

        # This regex gets the file name and method name for the missing
        #   parameter. The file name is the first group, and the method name
        #   is the second group.
        # TODO: This regex requires the first character of the captured file
        #   path to be '/'. This is because the command's stderr output is
        #   redirected to stdout, which can cause the output to be mangled (e.g.
        #   the error line may include some stdout output). The way the regex
        #   is currently written will work on Linux but will need to be adjusted
        #   for Windows.
        self._missing_parameter_file_regex = \
            r"(\/[\w\d\/\.]+:\d+): (?:warning|error): The following " + \
            r"parameter of (.*) is not documented:"

        # This regex gets the parameter name for the missing parameter. The
        #   parameter name is the first group.
        self._missing_parameter_param_regex = \
            r"parameter '([\w\d]+)'"


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
        if "The following parameter" in line and "is not documented" in line:
            return self._generate_missing_parameter_entry(
                line,
                next_lines,
                line_number
            )

        return None


    def _generate_missing_parameter_entry(self,
        line: str,
        next_lines: List[str],
        line_number: int) -> Entry:
        """
        Generates an entry for a missing parameter error.
        @param line The line to process.
        @param next_lines The next line(s) in the command output.
        @param line_number The line number of the line.
        @returns An entry for the line if an error is detected, otherwise None.
        """
        # Get the method with the missing parameter documentation
        assert len(next_lines) > 0
        file_match = re.search(self._missing_parameter_file_regex, line)
        param_match = re.search(
            self._missing_parameter_param_regex,
            next_lines[0]
        )

        assert file_match is not None
        assert param_match is not None

        # Extract the missing parameter info
        file_path = file_match.group(1)
        method_name = file_match.group(2)
        param_name = param_match.group(1)

        # Generate the entry
        return Entry(
            ESeverity.ERROR,
            line + "\n" + next_lines[0],
            line_number,
            line_number + 1,
            "[PyShell] Missing parameter documentation for:\n" + \
                "[PyShell]   File: " + file_path + "\n" + \
                "[PyShell]   Method: " + method_name + "\n" + \
                "[PyShell]   Parameter: " + param_name + "\n"
        )
