from __future__ import annotations
from pyshell.events.event_handler import EventHandler
import pytest
from typing import Callable, List, Optional

class EventHandlerFixture:
    def __init__(self):
        self.event_handler: EventHandler[EventHandlerFixture, int] = \
            EventHandler()
        self.observer_flags: List[bool] = []
        self.observer_senders: List[Optional[EventHandlerFixture]] = []
        self.observer_values: List[int] = []


    def make_observer(self, index: int) \
        -> Callable[[EventHandlerFixture, int], None]:
        """
        Helper method that creates an observer that sets a flag.
        @param index The index of the flag to set.
        @return The observer.
        """
        # Make sure a flag exists at the given index
        while len(self.observer_flags) <= index:
            self.observer_flags.append(False)

        # Make sure the sender list is long enough
        while len(self.observer_senders) <= index:
            self.observer_senders.append(None)

        # Make sure the value list is long enough
        while len(self.observer_values) <= index:
            self.observer_values.append(0)

        return lambda sender, args: self.on_broadcast(index, sender, args)


    def on_broadcast(self,
        index: int,
        sender: EventHandlerFixture,
        value: int):
        """
        Helper method used to implement an observer for test cases.
        @param index The index of the flag to set.
        @param sender The sender of the broadcast.
        @param value The value broadcast to the observer.
        """
        self.observer_flags[index] = True
        self.observer_senders[index] = sender
        self.observer_values[index] = value


@pytest.fixture
def fixture() -> EventHandlerFixture:
    return EventHandlerFixture()


def test_add_observer(fixture: EventHandlerFixture):
    fixture.event_handler.add_observer(lambda sender, args: None)


def test_broadcast_with_no_observers(fixture: EventHandlerFixture):
    fixture.event_handler.broadcast(fixture, 1)


def test_broadcast_with_one_observer(fixture: EventHandlerFixture):
    fixture.event_handler.add_observer(fixture.make_observer(0))
    fixture.event_handler.broadcast(fixture, 1)
    assert fixture.observer_flags[0]


def test_broadcast_with_multiple_observers(fixture: EventHandlerFixture):
    fixture.event_handler.add_observer(fixture.make_observer(0))
    fixture.event_handler.add_observer(fixture.make_observer(1))
    fixture.event_handler.broadcast(fixture, 1)
    assert fixture.observer_flags[0]
    assert fixture.observer_flags[1]


def test_single_observer_receives_broadcast_value(fixture: EventHandlerFixture):
    fixture.event_handler.add_observer(fixture.make_observer(0))
    fixture.event_handler.broadcast(fixture, 1)
    assert fixture.observer_senders[0] == fixture
    assert fixture.observer_values[0] == 1


def test_multiple_observers_receive_broadcast_value(fixture: EventHandlerFixture):
    fixture.event_handler.add_observer(fixture.make_observer(0))
    fixture.event_handler.add_observer(fixture.make_observer(1))
    fixture.event_handler.broadcast(fixture, 1)
    assert fixture.observer_senders[0] == fixture
    assert fixture.observer_values[0] == 1
    assert fixture.observer_senders[1] == fixture
    assert fixture.observer_values[1] == 1


def test_remove_observer(fixture: EventHandlerFixture):
    observer = fixture.make_observer(0)
    fixture.event_handler.add_observer(observer)
    assert fixture.event_handler.remove_observer(observer)
    fixture.event_handler.broadcast(fixture, 1)
    assert not fixture.observer_flags[0]


def test_remove_nonexistent_observer(fixture: EventHandlerFixture):
    observer = fixture.make_observer(0)
    assert not fixture.event_handler.remove_observer(observer)
