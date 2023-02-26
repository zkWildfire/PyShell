from pathlib import Path
from pyshell.core.pyshell import PyShell
from pyshell.core.pyshell_options import PyShellOptions
import pytest

def test_set_as_active_instance():
    pyshell = PyShell(
        set_as_active_instance=True
    )
    assert pyshell.active_instance() == pyshell


def test_skip_setting_as_active_instance():
    PyShell.clear_active_instance()
    pyshell = PyShell(
        set_as_active_instance=False
    )
    assert pyshell.active_instance() is None


def test_get_required_active_instance_with_active_instance_set():
    pyshell = PyShell(
        set_as_active_instance=True
    )
    assert pyshell.get_required_active_instance() is pyshell


def test_get_required_active_instance_without_active_instance_set():
    PyShell.clear_active_instance()
    with pytest.raises(ValueError):
        PyShell.get_required_active_instance()


def test_is_active_instance():
    pyshell = PyShell(
        set_as_active_instance=True
    )
    assert pyshell.is_active_instance()


def test_is_not_active_instance():
    PyShell.clear_active_instance()
    pyshell = PyShell(
        set_as_active_instance=False
    )
    assert not pyshell.is_active_instance()


def test_overwrite_active_instance():
    pyshell1 = PyShell(
        set_as_active_instance=True
    )
    pyshell2 = PyShell(
        set_as_active_instance=False
    )

    assert pyshell1.is_active_instance()
    assert not pyshell2.is_active_instance()

    pyshell2.set_as_active_instance()

    assert not pyshell1.is_active_instance()
    assert pyshell2.is_active_instance()


def test_cwd_defaults_to_script_cwd():
    pyshell = PyShell()
    assert pyshell.cwd == Path.cwd()
    assert pyshell.cwd.is_absolute()


def test_explicitly_set_cwd():
    pyshell = PyShell(cwd="/")
    assert pyshell.cwd == Path("/")
    assert pyshell.cwd.is_absolute()


def test_cd_with_absolute_path():
    pyshell = PyShell()
    pyshell.cd("/")
    assert pyshell.cwd == Path("/")
    assert pyshell.cwd.is_absolute()


def test_cd_with_relative_path():
    pyshell = PyShell()
    pyshell.cd("foo")
    assert pyshell.cwd == Path.cwd().joinpath("foo")
    assert pyshell.cwd.is_absolute()


def test_get_options():
    pyshell = PyShell(options=PyShellOptions(
        verbose=True
    ))
    assert pyshell.options.verbose
