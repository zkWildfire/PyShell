from pyshell.core.command_flags import CommandFlags
from pyshell.core.command_metadata import CommandMetadata

def test_command_properties_match_ctor_args():
    # Constants
    cmd_name = "foo"
    cmd_args = ["bar", "baz"]
    cmd_flags = CommandFlags.CLEANUP

    # Run the test
    cmd = CommandMetadata(cmd_name, cmd_args, cmd_flags)
    assert cmd.command == cmd_name
    assert cmd.args == cmd_args
    assert cmd.flags == cmd_flags


def test_full_command_on_command_with_no_args():
    cmd = CommandMetadata("foo", [])
    assert cmd.full_command == "foo"


def test_full_command_on_command_with_args():
    cmd = CommandMetadata("foo", ["bar", "baz"])
    assert cmd.full_command == "foo bar baz"


def test_standard_command():
    cmd = CommandMetadata("foo", ["bar", "baz"])
    assert not cmd.is_inactive
    assert not cmd.is_cleanup


def test_inactive_command():
    cmd = CommandMetadata("foo", ["bar", "baz"], CommandFlags.INACTIVE)
    assert cmd.is_inactive


def test_cleanup_command():
    cmd = CommandMetadata("foo", ["bar", "baz"], CommandFlags.CLEANUP)
    assert cmd.is_cleanup
