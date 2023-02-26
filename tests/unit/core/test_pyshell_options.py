from pyshell.core.pyshell_options import PyShellOptions

def test_properties_match_ctor_args():
    options = PyShellOptions(verbose=True)
    assert options.verbose
