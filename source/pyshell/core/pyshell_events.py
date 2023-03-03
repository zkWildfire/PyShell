from __future__ import annotations
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.command_result import CommandResult
from pyshell.events.event import Event
from pyshell.events.event_handler import EventHandler


class PyShellEvents:
    """
    Defines event handlers for each event that a PyShell instance can broadcast.
    This class is primarily used to avoid circular references by ensuring that
      PyShell components can bind to PyShell events without needing to import
      the PyShell class.
    """
    def __init__(self,
        on_command_started: EventHandler[PyShellEvents, CommandMetadata],
        on_command_skipped: EventHandler[PyShellEvents, CommandMetadata],
        on_command_finished: EventHandler[PyShellEvents, CommandResult],
        on_command_failed: EventHandler[PyShellEvents, CommandResult]):
        """
        Initializes the object.
        The objects this class wraps should be created by the PyShell class.
        @param on_command_started Event handler for the command_started event.
        @param on_command_skipped Event handler for the command_skipped event.
        @param on_command_finished Event handler for the command_finished event.
        @param on_command_failed Event handler for the command_failed event.
        """
        self.on_command_started = Event(on_command_started)
        self.on_command_skipped = Event(on_command_skipped)
        self.on_command_finished = Event(on_command_finished)
        self.on_command_failed = Event(on_command_failed)
