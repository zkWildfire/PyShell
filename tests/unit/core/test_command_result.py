from pyshell.core.command_result import CommandResult

def test_success_error_properties_on_successful_command():
    result = CommandResult(
        "foo",
        ["bar"],
        "/foo/bar",
        "baz",
        0
    )

    assert result.success
    assert not result.error


def test_success_error_properties_on_failed_command():
    result = CommandResult(
        "foo",
        ["bar"],
        "/foo/bar",
        "baz",
        1
    )

    assert not result.success
    assert result.error


def test_full_command_on_command_with_no_args():
    result = CommandResult(
        "foo",
        [],
        "/foo/bar",
        "baz",
        0
    )

    assert result.full_command == "foo"


def test_full_command_on_command_with_args():
    result = CommandResult(
        "foo",
        ["bar", "baz"],
        "/foo/bar",
        "baz",
        0
    )

    assert result.full_command == "foo bar baz"
