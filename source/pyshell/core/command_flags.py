from enum import IntEnum

class CommandFlags(IntEnum):
    """
    Flags that identify various properties of a command.
    """
    ## Helper value for commands that have no flags.
    NONE = 0x0

    ## Standard command, no special properties.
    STANDARD = 0x1

    ## The command's trigger condition has not been met.
    # Inactive commands should not be run.
    INACTIVE = 0x2

    ## Command is a command that should be run even if a failure occurs.
    CLEANUP = 0x4

    ## Don't log the command's output to any source.
    QUIET = 0x10

    ## Don't log the command's output to the console.
    NO_CONSOLE = 0x20

    ## Don't log the command's output to a file.
    NO_FILE = 0x40
