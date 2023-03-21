from datetime import datetime, timedelta
from dateutil import tz
from pyshell.commands.sync_command_result import SyncCommandResult
import pytest

def test_success_error_properties_on_successful_command():
    result = SyncCommandResult(
        "foo",
        ["bar"],
        "/foo/bar",
        "baz",
        0,
        False,
        datetime.now(),
        datetime.now()
    )

    assert result.success
    assert not result.error


def test_success_error_properties_on_failed_command():
    result = SyncCommandResult(
        "foo",
        ["bar"],
        "/foo/bar",
        "baz",
        1,
        False,
        datetime.now(),
        datetime.now()
    )

    assert not result.success
    assert result.error


def test_full_command_on_command_with_no_args():
    result = SyncCommandResult(
        "foo",
        [],
        "/foo/bar",
        "baz",
        0,
        False,
        datetime.now(),
        datetime.now()
    )

    assert result.full_command == "foo"


def test_full_command_on_command_with_args():
    result = SyncCommandResult(
        "foo",
        ["bar", "baz"],
        "/foo/bar",
        "baz",
        0,
        False,
        datetime.now(),
        datetime.now()
    )

    assert result.full_command == "foo bar baz"


def test_skipped_command():
    result = SyncCommandResult(
        "foo",
        ["bar", "baz"],
        "/foo/bar",
        "baz",
        0,
        True,
        datetime.now(),
        datetime.now()
    )

    assert result.skipped
    assert not result.success
    assert not result.error
    assert result.full_command == "foo bar baz"
    with pytest.raises(RuntimeError):
        result.exit_code


def test_successful_command_is_true():
    result = SyncCommandResult(
        "foo",
        ["bar", "baz"],
        "/foo/bar",
        "baz",
        0,
        False,
        datetime.now(),
        datetime.now()
    )

    assert result


def test_failed_command_is_false():
    result = SyncCommandResult(
        "foo",
        ["bar", "baz"],
        "/foo/bar",
        "baz",
        1,
        False,
        datetime.now(),
        datetime.now()
    )

    assert not result


def test_command_start_time():
    start_time = datetime.utcnow()
    result = SyncCommandResult(
        "foo",
        ["bar", "baz"],
        "/foo/bar",
        "baz",
        1,
        False,
        start_time,
        datetime.utcnow()
    )

    assert result.start_time_utc == start_time.astimezone(tz.tzutc())
    assert result.start_time_local == start_time.astimezone(tz.tzlocal())


def test_command_end_time():
    end_time = datetime.utcnow()
    result = SyncCommandResult(
        "foo",
        ["bar", "baz"],
        "/foo/bar",
        "baz",
        1,
        False,
        datetime.utcnow(),
        end_time
    )

    assert result.end_time_utc == end_time.astimezone(tz.tzutc())
    assert result.end_time_local == end_time.astimezone(tz.tzlocal())


def test_command_duration_seconds():
    duration = timedelta(seconds=1)
    start_time = datetime.now() - duration
    end_time = datetime.now()
    result = SyncCommandResult(
        "foo",
        ["bar", "baz"],
        "/foo/bar",
        "baz",
        1,
        False,
        start_time,
        end_time
    )

    # pyright: reportUnknownMemberType=false
    assert pytest.approx(result.duration_seconds, 0.1) == duration.total_seconds()


def test_command_duration_milliseconds():
    duration = timedelta(milliseconds=1)
    start_time = datetime.now() - duration
    end_time = datetime.now()
    result = SyncCommandResult(
        "foo",
        ["bar", "baz"],
        "/foo/bar",
        "baz",
        1,
        False,
        start_time,
        end_time
    )

    # pyright: reportUnknownMemberType=false
    assert pytest.approx(result.duration_milliseconds, 0.1) == \
        duration.total_seconds() * 1000


def test_command_duration_minutes():
    duration = timedelta(minutes=1)
    start_time = datetime.now() - duration
    end_time = datetime.now()
    result = SyncCommandResult(
        "foo",
        ["bar", "baz"],
        "/foo/bar",
        "baz",
        1,
        False,
        start_time,
        end_time
    )

    # pyright: reportUnknownMemberType=false
    assert pytest.approx(result.duration_minutes, 0.1) == \
        duration.total_seconds() / 60


def test_backend_property():
    backend = "FOOBAR"
    result = SyncCommandResult(
        "foo",
        ["bar", "baz"],
        "/foo/bar",
        "baz",
        1,
        False,
        datetime.now(),
        datetime.now(),
        backend
    )

    assert result.backend == backend
