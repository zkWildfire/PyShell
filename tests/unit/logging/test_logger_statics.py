from datetime import datetime, timedelta
import os
from pathlib import Path
from pyshell.commands.command_metadata import CommandMetadata
from pyshell.commands.sync_command_result import SyncCommandResult
from pyshell.logging.logger_options import LoggerOptions
from pyshell.logging.logger_statics import LoggerStatics


def test_write_header():
    cmd = "foo"
    args = ["bar", "baz"]
    metadata = CommandMetadata(
        cmd,
        args
    )
    cwd = Path.cwd()
    output = ""

    def write_callback(data: str):
        nonlocal output
        output += data

    LoggerStatics.write_command_header(metadata, cwd, write_callback)

    assert "Running command" in output
    assert cmd in output
    for arg in args:
        assert arg in output
    assert "cwd" in output
    assert str(cwd) in output

    # Make sure the `[PyShell]` tag doesn't get written twice
    assert output.count("[PyShell] [PyShell]") == 0


def test_write_footer():
    cmd = "foo"
    args = ["bar", "baz"]
    exit_code = 1
    cwd = os.getcwd()
    start_time = datetime.now()
    end_time = datetime.now() + timedelta(seconds=1)
    backend = "FOOBAR"

    result = SyncCommandResult(
        cmd,
        args,
        cwd,
        "",
        exit_code,
        False,
        start_time,
        end_time,
        backend
    )

    output = ""
    def write_callback(data: str):
        nonlocal output
        output += data

    LoggerStatics.write_command_footer(result, write_callback)

    assert "Executed command" in output
    assert "Backend" in output
    assert backend in output
    assert "cwd" in output
    assert cwd in output
    assert "Command exited with code" in output
    assert str(exit_code) in output
    assert "Start time" in output
    assert "End time" in output
    assert "Duration" in output

    # Make sure the `[PyShell]` tag doesn't get written twice
    assert output.count("[PyShell] [PyShell]") == 0


def test_write_only_cmd_in_header():
    cmd = "foo"
    args = []
    metadata = CommandMetadata(
        cmd,
        args
    )
    cwd = Path.cwd()
    output = ""

    def write_callback(data: str):
        nonlocal output
        output += data

    LoggerStatics.write_command_header(
        metadata,
        cwd,
        write_callback,
        LoggerOptions(
            print_cmd=True,
            print_cwd=False,
            print_backend=False,
            print_exit_code=False,
            print_timestamps=False,
            print_duration=False,
            add_newline_after_header=False,
            add_newline_before_footer=False,
            add_newline_after_footer=False
        )
    )

    assert "Running command" in output
    assert cmd in output
    assert not "cwd" in output
    assert not str(cwd) in output


def test_write_only_cwd_in_header():
    cmd = "foo"
    args = []
    metadata = CommandMetadata(
        cmd,
        args
    )
    cwd = Path.cwd()
    output = ""

    def write_callback(data: str):
        nonlocal output
        output += data

    LoggerStatics.write_command_header(
        metadata,
        cwd,
        write_callback,
        LoggerOptions(
            print_cmd=False,
            print_cwd=True,
            print_backend=False,
            print_exit_code=False,
            print_timestamps=False,
            print_duration=False,
            add_newline_after_header=False,
            add_newline_before_footer=False,
            add_newline_after_footer=False
        )
    )

    assert not "Running command" in output
    assert not cmd in output
    assert "cwd" in output
    assert str(cwd) in output


def test_write_custom_header_banner():
    cmd = "foo"
    args = ["bar", "baz"]
    metadata = CommandMetadata(
        cmd,
        args
    )
    cwd = Path.cwd()
    output = ""

    def write_callback(data: str):
        nonlocal output
        output += data

    char = "X"
    length = 5
    LoggerStatics.write_command_header(
        metadata,
        cwd,
        write_callback,
        LoggerOptions(
            print_cmd=True,
            print_cwd=True,
            print_backend=False,
            print_exit_code=False,
            print_timestamps=False,
            print_duration=False,
            add_newline_after_header=False,
            add_newline_before_footer=False,
            add_newline_after_footer=False,
            cmd_header_banner_char=char,
            cmd_header_banner_width=length
        )
    )

    assert output.strip().startswith(char * length)
    assert output.strip().endswith(char * length)


def test_write_only_cmd_in_footer():
    cmd = "foo"
    args = []
    exit_code = 1
    cwd = os.getcwd()
    start_time = datetime.now()
    end_time = datetime.now() + timedelta(seconds=1)
    backend = "FOOBAR"

    result = SyncCommandResult(
        cmd,
        args,
        cwd,
        "",
        exit_code,
        False,
        start_time,
        end_time,
        backend
    )

    output = ""
    def write_callback(data: str):
        nonlocal output
        output += data

    LoggerStatics.write_command_footer(
        result,
        write_callback,
        LoggerOptions(
            print_cmd=True,
            print_cwd=False,
            print_backend=False,
            print_exit_code=False,
            print_timestamps=False,
            print_duration=False,
            add_newline_after_header=False,
            add_newline_before_footer=False,
            add_newline_after_footer=False
        )
    )

    assert "Executed command" in output
    assert cmd in output
    assert not "Backend" in output
    assert not backend in output
    assert not "cwd" in output
    assert not cwd in output
    assert not "Command exited with code" in output
    assert not str(exit_code) in output
    assert not "Start time" in output
    assert not "End time" in output
    assert not "Duration" in output


def test_write_only_cwd_in_footer():
    cmd = "foo"
    args = []
    exit_code = 1
    cwd = os.getcwd()
    start_time = datetime.now()
    end_time = datetime.now() + timedelta(seconds=1)
    backend = "FOOBAR"

    result = SyncCommandResult(
        cmd,
        args,
        cwd,
        "",
        exit_code,
        False,
        start_time,
        end_time,
        backend
    )

    output = ""
    def write_callback(data: str):
        nonlocal output
        output += data

    LoggerStatics.write_command_footer(
        result,
        write_callback,
        LoggerOptions(
            print_cmd=False,
            print_cwd=True,
            print_backend=False,
            print_exit_code=False,
            print_timestamps=False,
            print_duration=False,
            add_newline_after_header=False,
            add_newline_before_footer=False,
            add_newline_after_footer=False
        )
    )

    assert not "Executed command" in output
    assert not cmd in output
    assert not "Backend" in output
    assert not backend in output
    assert "cwd" in output
    assert cwd in output
    assert not "Command exited with code" in output
    assert not str(exit_code) in output
    assert not "Start time" in output
    assert not "End time" in output
    assert not "Duration" in output


def test_write_only_backend_in_footer():
    cmd = "foo"
    args = []
    exit_code = 1
    cwd = os.getcwd()
    start_time = datetime.now()
    end_time = datetime.now() + timedelta(seconds=1)
    backend = "FOOBAR"

    result = SyncCommandResult(
        cmd,
        args,
        cwd,
        "",
        exit_code,
        False,
        start_time,
        end_time,
        backend
    )

    output = ""
    def write_callback(data: str):
        nonlocal output
        output += data

    LoggerStatics.write_command_footer(
        result,
        write_callback,
        LoggerOptions(
            print_cmd=False,
            print_cwd=False,
            print_backend=True,
            print_exit_code=False,
            print_timestamps=False,
            print_duration=False,
            add_newline_after_header=False,
            add_newline_before_footer=False,
            add_newline_after_footer=False
        )
    )

    assert not "Executed command" in output
    assert not cmd in output
    assert "Backend" in output
    assert backend in output
    assert not "cwd" in output
    assert not cwd in output
    assert not "Command exited with code" in output
    assert not str(exit_code) in output
    assert not "Start time" in output
    assert not "End time" in output
    assert not "Duration" in output


def test_write_only_exit_code_in_footer():
    cmd = "foo"
    args = []
    exit_code = 1
    cwd = os.getcwd()
    start_time = datetime.now()
    end_time = datetime.now() + timedelta(seconds=1)
    backend = "FOOBAR"

    result = SyncCommandResult(
        cmd,
        args,
        cwd,
        "",
        exit_code,
        False,
        start_time,
        end_time,
        backend
    )

    output = ""
    def write_callback(data: str):
        nonlocal output
        output += data

    LoggerStatics.write_command_footer(
        result,
        write_callback,
        LoggerOptions(
            print_cmd=False,
            print_cwd=False,
            print_backend=False,
            print_exit_code=True,
            print_timestamps=False,
            print_duration=False,
            add_newline_after_header=False,
            add_newline_before_footer=False,
            add_newline_after_footer=False
        )
    )

    assert not "Executed command" in output
    assert not cmd in output
    assert not "Backend" in output
    assert not backend in output
    assert not "cwd" in output
    assert not cwd in output
    assert "Command exited with code" in output
    assert str(exit_code) in output
    assert not "Start time" in output
    assert not "End time" in output
    assert not "Duration" in output


def test_write_only_timestamps_in_footer():
    cmd = "foo"
    args = []
    exit_code = 123456789
    cwd = os.getcwd()
    start_time = datetime.now()
    end_time = datetime.now() + timedelta(seconds=1)
    backend = "FOOBAR"

    result = SyncCommandResult(
        cmd,
        args,
        cwd,
        "",
        exit_code,
        False,
        start_time,
        end_time,
        backend
    )

    output = ""
    def write_callback(data: str):
        nonlocal output
        output += data

    LoggerStatics.write_command_footer(
        result,
        write_callback,
        LoggerOptions(
            print_cmd=False,
            print_cwd=False,
            print_backend=False,
            print_exit_code=False,
            print_timestamps=True,
            print_duration=False,
            add_newline_after_header=False,
            add_newline_before_footer=False,
            add_newline_after_footer=False
        )
    )

    assert not "Executed command" in output
    assert not cmd in output
    assert not "Backend" in output
    assert not backend in output
    assert not "cwd" in output
    assert not cwd in output
    assert not "Command exited with code" in output
    assert not str(exit_code) in output
    assert "Start time" in output
    assert "End time" in output
    assert not "Duration" in output


def test_write_only_duration_in_footer():
    cmd = "foo"
    args = []
    exit_code = 123456789
    cwd = os.getcwd()
    start_time = datetime.now()
    end_time = datetime.now() + timedelta(seconds=1)
    backend = "FOOBAR"

    results = [
        SyncCommandResult(
            cmd,
            args,
            cwd,
            "",
            exit_code,
            False,
            start_time,
            end_time,
            backend
        ),
        SyncCommandResult(
            cmd,
            args,
            cwd,
            "",
            exit_code,
            False,
            start_time,
            end_time + timedelta(seconds=30),
            backend
        ),
        SyncCommandResult(
            cmd,
            args,
            cwd,
            "",
            exit_code,
            False,
            start_time,
            end_time + timedelta(minutes=30),
            backend
        )
    ]

    output = ""
    def write_callback(data: str):
        nonlocal output
        output += data

    options = LoggerOptions(
        print_cmd=False,
        print_cwd=False,
        print_backend=False,
        print_exit_code=False,
        print_timestamps=False,
        print_duration=True,
        add_newline_after_header=False,
        add_newline_before_footer=False,
        add_newline_after_footer=False
    )
    for result in results:
        LoggerStatics.write_command_footer(
            result,
            write_callback,
            options
        )

    assert not "Executed command" in output
    assert not cmd in output
    assert not "Backend" in output
    assert not backend in output
    assert not "cwd" in output
    assert not cwd in output
    assert not "Command exited with code" in output
    assert not str(exit_code) in output
    assert not "Start time" in output
    assert not "End time" in output
    assert "Duration" in output


def test_write_custom_footer_banner():
    cmd = "foo"
    args = []
    exit_code = 1
    cwd = os.getcwd()
    start_time = datetime.now()
    end_time = datetime.now() + timedelta(seconds=1)
    backend = "FOOBAR"

    result = SyncCommandResult(
        cmd,
        args,
        cwd,
        "",
        exit_code,
        False,
        start_time,
        end_time,
        backend
    )

    output = ""
    def write_callback(data: str):
        nonlocal output
        output += data

    char = "X"
    length = 5
    LoggerStatics.write_command_footer(
        result,
        write_callback,
        LoggerOptions(
            print_cmd=True,
            print_cwd=False,
            print_backend=False,
            print_exit_code=False,
            print_timestamps=False,
            print_duration=False,
            add_newline_after_header=False,
            add_newline_before_footer=False,
            add_newline_after_footer=False,
            cmd_footer_banner_char=char,
            cmd_footer_banner_width=length
        )
    )

    assert output.strip().startswith(char * length)
    assert output.strip().endswith(char * length)


def test_header_skipped_if_no_components_enabled():
    cmd = "foo"
    args = ["bar", "baz"]
    metadata = CommandMetadata(
        cmd,
        args
    )
    cwd = Path.cwd()
    output = ""

    def write_callback(data: str):
        nonlocal output
        output += data

    LoggerStatics.write_command_header(
        metadata,
        cwd,
        write_callback,
        LoggerOptions(
            print_cmd=False,
            print_cwd=False,
            print_backend=False,
            print_exit_code=False,
            print_timestamps=False,
            print_duration=False,
            add_newline_after_header=False,
            add_newline_before_footer=False,
            add_newline_after_footer=False
        )
    )

    assert output.strip() == ""


def test_footer_skipped_if_no_components_enabled():
    cmd = "foo"
    args = []
    exit_code = 1
    cwd = os.getcwd()
    start_time = datetime.now()
    end_time = datetime.now() + timedelta(seconds=1)
    backend = "FOOBAR"

    result = SyncCommandResult(
        cmd,
        args,
        cwd,
        "",
        exit_code,
        False,
        start_time,
        end_time,
        backend
    )

    output = ""
    def write_callback(data: str):
        nonlocal output
        output += data

    LoggerStatics.write_command_footer(
        result,
        write_callback,
        LoggerOptions(
            print_cmd=False,
            print_cwd=False,
            print_backend=False,
            print_exit_code=False,
            print_timestamps=False,
            print_duration=False,
            add_newline_after_header=False,
            add_newline_before_footer=False,
            add_newline_after_footer=False
        )
    )

    assert output.strip() == ""


def test_append_newline_after_headers():
    cmd = "foo"
    args = []
    exit_code = 1
    cwd = os.getcwd()
    start_time = datetime.now()
    end_time = datetime.now() + timedelta(seconds=1)
    backend = "FOOBAR"

    result = SyncCommandResult(
        cmd,
        args,
        cwd,
        "",
        exit_code,
        False,
        start_time,
        end_time,
        backend
    )

    output = ""
    def write_callback(data: str):
        nonlocal output
        output += data

    LoggerStatics.write_command_footer(
        result,
        write_callback,
        LoggerOptions(
            print_cmd=True,
            print_cwd=False,
            print_backend=False,
            print_exit_code=False,
            print_timestamps=False,
            print_duration=False,
            add_newline_after_header=True,
            add_newline_before_footer=False,
            add_newline_after_footer=False
        )
    )

    assert output.endswith("\n")


def test_append_newline_before_footer():
    cmd = "foo"
    args = []
    exit_code = 1
    cwd = os.getcwd()
    start_time = datetime.now()
    end_time = datetime.now() + timedelta(seconds=1)
    backend = "FOOBAR"

    result = SyncCommandResult(
        cmd,
        args,
        cwd,
        "",
        exit_code,
        False,
        start_time,
        end_time,
        backend
    )

    output = ""
    def write_callback(data: str):
        nonlocal output
        output += data

    LoggerStatics.write_command_footer(
        result,
        write_callback,
        LoggerOptions(
            print_cmd=True,
            print_cwd=False,
            print_backend=False,
            print_exit_code=False,
            print_timestamps=False,
            print_duration=False,
            add_newline_after_header=False,
            add_newline_before_footer=True,
            add_newline_after_footer=False
        )
    )

    assert output.startswith("\n")


def test_append_newline_after_footer():
    cmd = "foo"
    args = []
    exit_code = 1
    cwd = os.getcwd()
    start_time = datetime.now()
    end_time = datetime.now() + timedelta(seconds=1)
    backend = "FOOBAR"

    result = SyncCommandResult(
        cmd,
        args,
        cwd,
        "",
        exit_code,
        False,
        start_time,
        end_time,
        backend
    )

    output = ""
    def write_callback(data: str):
        nonlocal output
        output += data

    LoggerStatics.write_command_footer(
        result,
        write_callback,
        LoggerOptions(
            print_cmd=True,
            print_cwd=False,
            print_backend=False,
            print_exit_code=False,
            print_timestamps=False,
            print_duration=False,
            add_newline_after_header=False,
            add_newline_before_footer=False,
            add_newline_after_footer=True
        )
    )

    assert output.endswith("\n")
