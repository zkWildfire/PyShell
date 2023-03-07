from pyshell.logging.logger_options import LoggerOptions

def test_properties_match_ctor_args():
    # Each of these values should be the opposite of the constructor parameter's
    #   default value
    print_cmd = False
    print_cwd = False
    print_backend = False
    print_exit_code = False
    print_timestamps = False
    print_duration = False
    add_newline_after_header = False
    add_newline_before_footer = False
    add_newline_after_footer = False
    cmd_header_banner_char = "h"
    cmd_header_banner_width = 10
    cmd_footer_banner_char = "f"
    cmd_footer_banner_width = 10
    cmd_header_banner_prefix = "p"
    cmd_footer_banner_prefix = "q"

    # Set up the options instance
    logger_options = LoggerOptions(
        print_cmd=print_cmd,
        print_cwd=print_cwd,
        print_backend=print_backend,
        print_exit_code=print_exit_code,
        print_timestamps=print_timestamps,
        print_duration=print_duration,
        add_newline_after_header=add_newline_after_header,
        add_newline_before_footer=add_newline_before_footer,
        add_newline_after_footer=add_newline_after_footer,
        cmd_header_banner_char=cmd_header_banner_char,
        cmd_header_banner_width=cmd_header_banner_width,
        cmd_footer_banner_char=cmd_footer_banner_char,
        cmd_footer_banner_width=cmd_footer_banner_width,
        cmd_header_banner_prefix=cmd_header_banner_prefix,
        cmd_footer_banner_prefix=cmd_footer_banner_prefix
    )

    # Validate the properties
    assert logger_options.print_cmd == print_cmd
    assert logger_options.print_cwd == print_cwd
    assert logger_options.print_backend == print_backend
    assert logger_options.print_exit_code == print_exit_code
    assert logger_options.print_timestamps == print_timestamps
    assert logger_options.print_duration == print_duration
    assert logger_options.add_newline_after_header == add_newline_after_header
    assert logger_options.add_newline_before_footer == add_newline_before_footer
    assert logger_options.add_newline_after_footer == add_newline_after_footer
    assert logger_options.cmd_header_banner_char == cmd_header_banner_char
    assert logger_options.cmd_header_banner_width == cmd_header_banner_width
    assert logger_options.cmd_footer_banner_char == cmd_footer_banner_char
    assert logger_options.cmd_footer_banner_width == cmd_footer_banner_width
    assert logger_options.cmd_header_banner_prefix == cmd_header_banner_prefix
    assert logger_options.cmd_footer_banner_prefix == cmd_footer_banner_prefix


def test_header_banner():
    # Set up the options instance
    char = "h"
    length = 10

    logger_options = LoggerOptions(
        cmd_header_banner_char=char,
        cmd_header_banner_width=length
    )

    # Validate the properties
    assert logger_options.cmd_header_banner == char * length


def test_footer_banner():
    # Set up the options instance
    char = "f"
    length = 10

    logger_options = LoggerOptions(
        cmd_footer_banner_char=char,
        cmd_footer_banner_width=length
    )

    # Validate the properties
    assert logger_options.cmd_footer_banner == char * length
