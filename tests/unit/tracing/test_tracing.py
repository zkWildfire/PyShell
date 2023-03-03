from pathlib import Path
from pyshell.shell.ls_command import LsCommand
from pyshell.tracing.caller_info import CallerInfo
import pytest
from unit.tracing.get_caller_line_number import get_caller_line_number

def test_closest_external_frame():
    """
    Verifies that the `closest_external_frame()` method returns a caller info
      capturing this method.
    """
    caller_info = CallerInfo.closest_external_frame()
    expected_line_number = get_caller_line_number() - 1

    assert str(caller_info.file_path) == __file__
    assert caller_info.line_number == expected_line_number


def test_from_stack_frame():
    """
    Verifies that this method's stack frame can be captured using
      `CallerInfo.from_stack_frame()`
    """
    caller_info = CallerInfo.from_stack_frame(0)
    expected_line_number = get_caller_line_number() - 1

    assert str(caller_info.file_path) == __file__
    assert caller_info.line_number == expected_line_number


def test_hash_and_equality():
    caller_info1 = CallerInfo(Path("/foo.py"), 1)
    caller_info2 = CallerInfo(Path("/foo.py"), 1)
    assert caller_info1 == caller_info2
    assert hash(caller_info1) == hash(caller_info2)

    caller_info3 = CallerInfo(Path("/bar.py"), 1)
    assert caller_info1 != caller_info3
    assert hash(caller_info1) != hash(caller_info3)

    caller_info4 = CallerInfo(Path("/foo.py"), 2)
    assert caller_info1 != caller_info4
    assert hash(caller_info1) != hash(caller_info4)

    assert caller_info1 != 1
    assert caller_info1 != "foo"
    assert caller_info1 != None


def test_ctor_throws_if_path_not_absolute():
    with pytest.raises(ValueError):
        CallerInfo("foo.py", 1)


def test_get_caller_stack_frame_from_multiple_levels_down():
    """
    Verifies that when the caller stack frame is obtained from a PyShell method
      invoked from another PyShell method, the resulting caller info captures
      the stack frame of the external method that resulted in the stack frame
      getting captured.
    """
    # Creating this command will capture a stack frame, which will be done from
    #   within a method invoked by the command's constructor
    command = LsCommand()
    expected_line_number = get_caller_line_number() - 1

    assert command.origin.file_path == Path(__file__)
    assert command.origin.line_number == expected_line_number
