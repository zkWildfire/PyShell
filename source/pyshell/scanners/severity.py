from enum import IntEnum

class ESeverity(IntEnum):
    """
    Defines the severity of a scanner's output.
    """
    ## Lowest severity level.
    # Entries with this severity should only be printed when using the highest
    #   verbosity level.
    VERBOSE = 0

    ## Debug message.
    # This severity level is placed above the VERBOSE level so that it can be
    #   used to print debug messages without having to use sift through verbose
    #   messages.
    DEBUG = 1

    ## Informational only.
    # This is the default severity level for scanner entries.
    INFO = 2

    ## Alerts the user of a potential issue.
    # This severity level should be used to alert the user if something is
    #   detected that may be an issue but is not an outright error.
    WARNING = 3

    ## Alerts the user of a non-fatal error.
    # This severity level should be used to alert the user if something is
    #   detected that is definitely a error. This severity level should be used
    #   if an error is detected but the program can continue to run, e.g. errors
    #   that will cause the program to exit with a non-zero exit code once it's
    #   done running.
    ERROR = 4

    ## Alerts the user of a critical error.
    # This severity level should be used to alert the user if something is
    #   detected that is so severe that the program exits immediately.
    CRITICAL = 5
