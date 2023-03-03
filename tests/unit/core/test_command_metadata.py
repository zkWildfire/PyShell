from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.command_metadata import CommandMetadata

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
    assert cmd.is_standard
    assert not cmd.is_inactive
    assert not cmd.is_cleanup


def test_inactive_command():
    cmd = CommandMetadata("foo", ["bar", "baz"], CommandFlags.INACTIVE)
    assert not cmd.is_standard
    assert cmd.is_inactive
    assert not cmd.is_cleanup


def test_cleanup_command():
    cmd = CommandMetadata("foo", ["bar", "baz"], CommandFlags.CLEANUP)
    assert not cmd.is_standard
    assert not cmd.is_inactive
    assert cmd.is_cleanup
