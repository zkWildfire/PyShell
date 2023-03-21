from datetime import datetime
from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.command_helpers import enable_if
from pyshell.commands.sync_command_result import SyncCommandResult

def test_enable_if_boolean():
    assert enable_if(True) == CommandFlags.STANDARD
    assert enable_if(False) == CommandFlags.INACTIVE


def test_enable_if_command_result():
    success_result = SyncCommandResult(
        "command",
        [],
        "",
        "",
        0,
        False,
        datetime.now(),
        datetime.now()
    )
    failed_result = SyncCommandResult(
        "command",
        [],
        "",
        "",
        1,
        False,
        datetime.now(),
        datetime.now()
    )

    assert enable_if(success_result) == CommandFlags.STANDARD
    assert enable_if(failed_result) == CommandFlags.INACTIVE
