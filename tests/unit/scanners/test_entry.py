from pyshell.scanners.entry import Entry
from pyshell.scanners.severity import ESeverity


def test_entry_properties_match_ctor_args():
    # Constants
    severity = ESeverity.WARNING
    cmd_output = "foo"
    start_line = 1
    end_line = 2
    scanner_output = "bar"

    # Run the test
    entry = Entry(severity, cmd_output, start_line, end_line, scanner_output)
    assert entry.severity == severity
    assert entry.cmd_output == cmd_output
    assert entry.start_line == start_line
    assert entry.end_line == end_line
    assert entry.scanner_output == scanner_output
