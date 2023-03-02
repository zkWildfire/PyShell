from enum import Enum

class StreamConfig(Enum):
    """
    Allows a logger to specify how the command's streams should be configured.
    """
    ## Keep stdout and stderr separate.
    SPLIT_STREAMS = 0

    ## Redirect stderr to stdout.
    MERGED_STREAMS = 1
