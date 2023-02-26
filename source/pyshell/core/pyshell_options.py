class PyShellOptions:
    """
    Defines options for a PyShell instance.
    These options may be read by PyShell commands to determine how they should
      behave.
    """
    def __init__(self,
        verbose: bool = False):
        """
        Initializes the object.
        @param verbose Whether verbose mode is enabled.
        """
        self._verbose = verbose


    @property
    def verbose(self) -> bool:
        """
        Whether verbose mode is enabled.
        """
        return self._verbose
