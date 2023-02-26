from pyshell.core.command_result import CommandResult
from pyshell.doxygen.doxygen_scanner import DoxygenScanner
from pyshell.scanners.severity import ESeverity

def test_scan_log_with_no_errors():
    scanner = DoxygenScanner()
    result = CommandResult(
        "doxygen",
        ["doxyfile"],
        "/foo/bar",
        "foo\nbar\nbaz",
        0,
        False
    )
    assert not scanner.scan_for_errors(result)


def test_scan_log_with_single_missing_parameter_error():
    # Constants
    file = "/workspaces/PyShell/source/pyshell/doxygen/doxygen_scanner.py:80"
    method = "pyshell.doxygen.doxygen_scanner.DoxygenScanner." + \
        "_generate_missing_parameter_entry(self, " + \
        "str line, List[str] next_lines, int line_number)"
    parameter = "line"

    # Run the test
    scanner = DoxygenScanner()
    result = CommandResult(
        "doxygen",
        ["doxyfile"],
        "/foo/bar",
        f"{file}: warning: The following parameter of " +
        f"{method} is not documented:\n" +
        f"parameter '{parameter}'",
        1,
        False
    )
    entries = scanner.scan_for_errors(result)

    # Validate results
    assert len(entries) == 1
    entry = entries[0]
    assert entry.severity == ESeverity.ERROR
    assert file in entry.cmd_output
    assert method in entry.cmd_output
    assert parameter in entry.cmd_output


def test_scan_log_with_mangled_missing_parameter_error():
    # Constants
    file = "/workspaces/PyShell/source/pyshell/doxygen/doxygen_scanner.py:80"
    method = "pyshell.doxygen.doxygen_scanner.DoxygenScanner." + \
        "_generate_missing_parameter_entry(self, " + \
        "str line, List[str] next_lines, int line_number)"
    parameter = "line"

    # Run the test
    scanner = DoxygenScanner()
    result = CommandResult(
        "doxygen",
        ["doxyfile"],
        "/foo/bar",
        # This can happen as a result of the command's stderr output being
        #   redirected to stdout. Make sure the scanner still recognizes it.
        f"asdlkfjakdjfklads{file}: warning: The following parameter of " +
        f"{method} is not documented:\n" +
        f"parameter '{parameter}'",
        1,
        False
    )
    entries = scanner.scan_for_errors(result)

    # Validate result
    assert len(entries) == 1
    entry = entries[0]
    assert entry.severity == ESeverity.ERROR
    assert file in entry.cmd_output
    assert method in entry.cmd_output
    assert parameter in entry.cmd_output
