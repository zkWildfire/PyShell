from pyshell.core.pyshell_options import PyShellOptions
import pytest

def test_properties_match_ctor_args():
    options = PyShellOptions(verbose=True)
    assert options.verbose


@pytest.mark.parametrize("value", [True, False])
def test_verbosity_level_from_bool(value: bool):
    options = PyShellOptions(verbose=value)
    assert options.verbose == value
    assert options.verbosity_level == int(value)


@pytest.mark.parametrize("value", [0, 1, 2])
def test_verbosity_level_from_int(value: int):
    options = PyShellOptions(verbose=value)
    assert options.verbose == bool(value)
    assert options.verbosity_level == value
