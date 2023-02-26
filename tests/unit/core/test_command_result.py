from pyshell.core.command_result import CommandResult
import pytest

def test_success_error_properties_on_successful_command():
    result = CommandResult(
        "foo",
        ["bar"],
        "/foo/bar",
        "baz",
        0,
        False
    )

    assert result.success
    assert not result.error


def test_success_error_properties_on_failed_command():
    result = CommandResult(
        "foo",
        ["bar"],
        "/foo/bar",
        "baz",
        1,
        False
    )

    assert not result.success
    assert result.error


def test_full_command_on_command_with_no_args():
    result = CommandResult(
        "foo",
        [],
        "/foo/bar",
        "baz",
        0,
        False
    )

    assert result.full_command == "foo"


def test_full_command_on_command_with_args():
    result = CommandResult(
        "foo",
        ["bar", "baz"],
        "/foo/bar",
        "baz",
        0,
        False
    )

    assert result.full_command == "foo bar baz"


def test_skipped_command():
    result = CommandResult(
        "foo",
        ["bar", "baz"],
        "/foo/bar",
        "baz",
        0,
        True
    )

    assert result.skipped
    assert not result.success
    assert not result.error
    assert result.full_command == "foo bar baz"
    with pytest.raises(RuntimeError):
        result.exit_code
