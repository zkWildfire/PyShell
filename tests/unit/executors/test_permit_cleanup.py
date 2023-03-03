from pyshell.commands.command_flags import CommandFlags
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.command_result import CommandResult
from pyshell.core.pyshell_events import PyShellEvents
from pyshell.events.event_handler import EventHandler
from pyshell.executors.permit_cleanup import PermitCleanup
import pytest

class PermitCleanupFixture:
    def __init__(self):
        # Create the events that PyShell can broadcast to
        self.on_command_started: EventHandler[PyShellEvents, CommandMetadata] = \
            EventHandler()
        self.on_command_skipped: EventHandler[PyShellEvents, CommandMetadata] = \
            EventHandler()
        self.on_command_finished: EventHandler[PyShellEvents, CommandResult] = \
            EventHandler()
        self.on_command_failed: EventHandler[PyShellEvents, CommandResult] = \
            EventHandler()
        self.events = PyShellEvents(
            self.on_command_started,
            self.on_command_skipped,
            self.on_command_finished,
            self.on_command_failed
        )

        # Initialize the executor
        self.executor = PermitCleanup()
        self.executor.initialize(self.events)


@pytest.fixture
def fixture():
    return PermitCleanupFixture()


def test_allow_standard_command(fixture: PermitCleanupFixture):
    metadata = CommandMetadata("foo", [], CommandFlags.STANDARD)
    assert fixture.executor.should_run(metadata)


def test_block_inactive_command(fixture: PermitCleanupFixture):
    metadata = CommandMetadata("foo", [], CommandFlags.INACTIVE)
    assert not fixture.executor.should_run(metadata)


def test_allow_cleanup_command(fixture: PermitCleanupFixture):
    metadata = CommandMetadata("foo", [], CommandFlags.CLEANUP)
    assert fixture.executor.should_run(metadata)


def test_block_standard_command_after_failure(fixture: PermitCleanupFixture):
    metadata = CommandMetadata("foo", [], CommandFlags.STANDARD)

    # Simulate a command failure
    result = CommandResult(
        metadata.command,
        metadata.args,
        "/foo",
        "",
        1,
        False
    )
    fixture.on_command_failed.broadcast(fixture.events, result)

    # Standard commands should be blocked from running after a failure
    assert not fixture.executor.should_run(metadata)


def test_block_inactive_command_after_failure(fixture: PermitCleanupFixture):
    metadata = CommandMetadata("foo", [], CommandFlags.INACTIVE)

    # Simulate a command failure
    result = CommandResult(
        metadata.command,
        metadata.args,
        "/foo",
        "",
        1,
        False
    )
    fixture.on_command_failed.broadcast(fixture.events, result)

    # Inactive commands should be blocked from running after a failure
    assert not fixture.executor.should_run(metadata)


def test_allow_cleanup_command_after_failure(fixture: PermitCleanupFixture):
    metadata = CommandMetadata("foo", [], CommandFlags.CLEANUP)

    # Simulate a command failure
    result = CommandResult(
        metadata.command,
        metadata.args,
        "/foo",
        "",
        1,
        False
    )
    fixture.on_command_failed.broadcast(fixture.events, result)

    # Cleanup commands should be allowed to run after a failure
    assert fixture.executor.should_run(metadata)
