from abc import ABC
from pyshell.core.pyshell_events import PyShellEvents

class IPyShellComponent(ABC):
    """
    Base class for all components used by a PyShell instance.
    """
    def initialize(self, events: PyShellEvents) -> None:
        """
        Initializes the executor.
        @param events `PyShellEvents` instance for the pyshell instance that
          the executor is being used with.
        """
        pass
