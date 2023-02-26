# pyright: reportUnusedImport=false
from unit.events.event_handler_fixture import EventHandlerFixture, fixture

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
