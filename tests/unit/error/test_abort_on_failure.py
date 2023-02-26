import os
from pyshell.core.command_metadata import CommandMetadata
from pyshell.core.command_result import CommandResult
from pyshell.error.abort_on_failure import AbortOnFailure
import pytest

def test_handle_error_throws():
    handler = AbortOnFailure()
    with pytest.raises(RuntimeError):
        handler.handle(CommandResult(
            CommandMetadata("foo", []),
            os.getcwd(),
            "",
            1,
            False
        ))
