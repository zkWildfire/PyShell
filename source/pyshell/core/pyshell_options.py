from pyshell.logging.logger_options import LoggerOptions

class PyShellOptions:
    """
    Defines options for a PyShell instance.
    These options may be read by PyShell commands to determine how they should
      behave.
    """
    def __init__(self,
        verbose: bool | int = False,
        quiet: bool = False,
        logger_options: LoggerOptions = LoggerOptions()):
        """
        Initializes the object.
        @param verbose Whether verbose mode is enabled. Boolean values will be
          converted to 1 and 0 for True and False, respectively.
        @param quiet Whether to enable quiet mode for messages printed directly
          through the PyShell instance. If this is set, all messages printed
          directly through the PyShell instance will be suppressed regardless of
          the verbosity level. This does not affect messages printed through
          loggers.
        @param logger_options Options used to control logger output formatting.
        """
        if isinstance(verbose, bool):
            verbose = int(verbose)

        self._verbose = verbose
        self._quiet = quiet
        self._logger_options = logger_options


    @property
    def verbose(self) -> bool:
        """
        Whether verbose mode is enabled.
        """
        return bool(self._verbose)


    @property
    def verbosity_level(self) -> int:
        """
        The verbosity level.
        """
        return self._verbose


    @property
    def quiet(self) -> bool:
        """
        Whether quiet mode is enabled.
        """
        return self._quiet


    @property
    def logger_options(self) -> LoggerOptions:
        """
        Options used to control logger output formatting.
        """
        return self._logger_options
