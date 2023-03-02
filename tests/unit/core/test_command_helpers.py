from pyshell.core.command_flags import CommandFlags
from pyshell.core.command_helpers import enable_if
from pyshell.core.command_result import CommandResult

def test_enable_if_boolean():
    assert enable_if(True) == CommandFlags.STANDARD
    assert enable_if(False) == CommandFlags.INACTIVE


def test_enable_if_command_result():
    success_result = CommandResult("command", [], "", "", 0, False)
    failed_result = CommandResult("command", [], "", "", 1, False)

    assert enable_if(success_result) == CommandFlags.STANDARD
    assert enable_if(failed_result) == CommandFlags.INACTIVE
