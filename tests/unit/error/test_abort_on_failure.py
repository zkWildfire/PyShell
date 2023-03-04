from datetime import datetime
import os
from pyshell.commands.command_result import CommandResult
from pyshell.error.abort_on_failure import AbortOnFailure
import pytest

def test_handle_error_throws():
    handler = AbortOnFailure()
    with pytest.raises(RuntimeError):
        handler.handle(CommandResult(
            "foo",
            [],
            os.getcwd(),
            "",
            1,
            False,
            datetime.now(),
            datetime.now()
        ))
