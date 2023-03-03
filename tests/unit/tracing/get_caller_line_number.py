from inspect import currentframe, getframeinfo

def get_caller_line_number() -> int:
    """
    Helper method used to get the caller's line number.
    @returns The line number of the caller.
    """
    curr_frame = currentframe()
    assert curr_frame
    assert curr_frame.f_back
    return getframeinfo(curr_frame.f_back).lineno
