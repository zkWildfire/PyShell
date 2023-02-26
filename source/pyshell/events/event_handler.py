from typing import Callable, Generic, List, TypeVar

SenderType = TypeVar("SenderType")
ArgsType = TypeVar("ArgsType")

class EventHandler(Generic[SenderType, ArgsType]):
    """
    Provides full access to all event-related methods.
    This class should be thought of as being equivalent to C#'s `EventHandler`
      type.
    """
    def __init__(self):
        # List of observers that should be invoked when the event is broadcast to.
        # Each observer will be passed the object sending the event and the data
        #   associated with the event.
        self._observers: List[Callable[[SenderType, ArgsType], None]] = []


    def add_observer(self, observer: Callable[[SenderType, ArgsType], None]) \
        -> None:
        """
        Adds an observer to the event.
        @param observer The observer to add.
        """
        self._observers.append(observer)


    def broadcast(self, sender: SenderType, args: ArgsType) -> None:
        """
        Broadcasts the event to all observers.
        @warning Generally, this method should only be called by the object that
          owns the event.
        @param sender The object sending the event.
        @param args The data associated with the event.
        """
        for observer in self._observers:
            observer(sender, args)


    def remove_observer(self, observer: Callable[[SenderType, ArgsType], None]) \
        -> bool:
        """
        Removes an observer from the event.
        @param observer The observer to remove.
        @return True if the observer was removed, False if it was not found.
        """
        try:
            self._observers.remove(observer)
            return True
        except ValueError:
            return False
