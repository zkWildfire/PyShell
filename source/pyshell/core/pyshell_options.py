from typing import NamedTuple

class PyShellOptions(NamedTuple):
    """
    Defines options for a PyShell instance.
    These options may be read by PyShell commands to determine how they should
      behave.
    """
    # Whether verbose mode is enabled.
    verbose: bool = False
