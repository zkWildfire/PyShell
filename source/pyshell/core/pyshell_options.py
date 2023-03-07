from pyshell.logging.logger_options import LoggerOptions

class PyShellOptions:
    """
    Defines options for a PyShell instance.
    These options may be read by PyShell commands to determine how they should
      behave.
    """
    def __init__(self,
        verbose: bool = False,
        logger_options: LoggerOptions = LoggerOptions()):
        """
        Initializes the object.
        @param verbose Whether verbose mode is enabled.
        @param logger_options Options used to control logger output formatting.
        """
        self._verbose = verbose
        self._logger_options = logger_options


    @property
    def verbose(self) -> bool:
        """
        Whether verbose mode is enabled.
        """
        return self._verbose


    @property
    def logger_options(self) -> LoggerOptions:
        """
        Options used to control logger output formatting.
        """
        return self._logger_options
