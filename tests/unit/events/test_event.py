# pyright: reportUnusedImport=false
from pyshell.events.event import Event
from unit.events.event_handler_fixture import EventHandlerFixture, fixture

def test_add_observer(fixture: EventHandlerFixture):
    event: Event[EventHandlerFixture, int] = Event(fixture.event_handler)
    observer = fixture.make_observer(0)
    # Make sure these don't throw
    event.add_observer(lambda sender, args: None)
    event += observer


def test_broadcast_to_single_observer(fixture: EventHandlerFixture):
    event: Event[EventHandlerFixture, int] = Event(fixture.event_handler)
    observer = fixture.make_observer(0)
    event += observer
    fixture.event_handler.broadcast(fixture, 1)
    assert fixture.observer_flags[0]


def test_broadcast_to_multiple_observers(fixture: EventHandlerFixture):
    event: Event[EventHandlerFixture, int] = Event(fixture.event_handler)
    observer0 = fixture.make_observer(0)
    observer1 = fixture.make_observer(1)
    event += observer0
    event += observer1
    fixture.event_handler.broadcast(fixture, 1)
    assert fixture.observer_flags[0]
    assert fixture.observer_flags[1]


def test_remove_observer(fixture: EventHandlerFixture):
    event: Event[EventHandlerFixture, int] = Event(fixture.event_handler)
    observer = fixture.make_observer(0)
    event.add_observer(observer)
    assert event.remove_observer(observer)

    # Since the observer was removed, its flag should not be set when an event
    #   is broadcast.
    fixture.event_handler.broadcast(fixture, 1)
    assert not fixture.observer_flags[0]


def test_remove_nonexistent_observer(fixture: EventHandlerFixture):
    event: Event[EventHandlerFixture, int] = Event(fixture.event_handler)
    observer = fixture.make_observer(0)
    assert not event.remove_observer(observer)


def test_remove_observer_using_operator(fixture: EventHandlerFixture):
    event: Event[EventHandlerFixture, int] = Event(fixture.event_handler)
    observer = fixture.make_observer(0)
    event.add_observer(observer)
    event -= observer

    # Since the observer was removed, its flag should not be set when an event
    #   is broadcast.
    fixture.event_handler.broadcast(fixture, 1)
    assert not fixture.observer_flags[0]


def test_remove_nonexistent_observer_using_operator(fixture: EventHandlerFixture):
    event: Event[EventHandlerFixture, int] = Event(fixture.event_handler)
    observer = fixture.make_observer(0)
    event -= observer
