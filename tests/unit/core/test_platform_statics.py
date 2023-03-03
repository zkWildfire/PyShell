from pyshell.core.platform_statics import PlatformStatics
import pytest
import sys

def test_check_current_os():
    # PlatformStatics currently goes through a different API than sys.platform.
    #   Use sys.platform to verify that PlatformStatics is working correctly.
    assert PlatformStatics.is_linux() == (sys.platform == "linux")
    assert PlatformStatics.is_windows() == ("win" in sys.platform)


def test_find_executable_on_path():
    # Find a command that should be on the path
    exe_name = PlatformStatics.to_executable_name("echo")
    exe_path = PlatformStatics.resolve_using_path(exe_name)
    assert exe_path.name == exe_name


def test_find_executable_not_on_path():
    # Find a command that should not be on the path
    exe_name = PlatformStatics.to_executable_name("not_a_real_command")
    with pytest.raises(FileNotFoundError):
        PlatformStatics.resolve_using_path(exe_name)
