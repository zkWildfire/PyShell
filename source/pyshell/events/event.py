from __future__ import annotations
from pyshell.events.event_handler import EventHandler
from typing import Callable, Generic, TypeVar

SenderType = TypeVar("SenderType")
ArgsType = TypeVar("ArgsType")

class Event(Generic[SenderType, ArgsType]):
    """
    Class intended to be publicly exposed via a property.
    This class wraps an EventHandler and ensures that external code can only
      bind to the event and can't broadcast to it.
    """
    def __init__(self, event_handler: EventHandler[SenderType, ArgsType]):
        """
        Initializes the object.
        @param event_handler The `EventHandler` that will be wrapped.
        """
        self._event_handler = event_handler


    def __iadd__(self, observer: Callable[[SenderType, ArgsType], None]) \
        -> Event[SenderType, ArgsType]:
        """
        Adds an observer to the event.
        @param observer The observer to add.
        @return This object instance.
        """
        self._event_handler.add_observer(observer)
        return self


    def __isub__(self, observer: Callable[[SenderType, ArgsType], None]) \
        -> Event[SenderType, ArgsType]:
        """
        Removes an observer from the event.
        @param observer The observer to remove.
        @return This object instance.
        """
        self._event_handler.remove_observer(observer)
        return self


    def add_observer(self, observer: Callable[[SenderType, ArgsType], None]):
        """
        Adds an observer to the event.
        @param observer The observer to add.
        """
        self._event_handler.add_observer(observer)


    def remove_observer(self, observer: Callable[[SenderType, ArgsType], None]) \
        -> bool:
        """
        Removes an observer from the event.
        @param observer The observer to remove.
        @return True if the observer was removed, False if it was not found.
        """
        return self._event_handler.remove_observer(observer)
