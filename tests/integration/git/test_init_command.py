from pathlib import Path
from pyshell import PyShell
from pyshell.modules.git import Git
from typing import Any

def test_init_command_in_empty_dir(tmp_path: Any):
    # Set up a shell in the temporary directory
    pyshell = PyShell()
    pyshell.cd(tmp_path)

    # Run the command
    result = Git.init()
    assert result.success
    assert Path(tmp_path, ".git").exists()


def test_init_nonstandard_branch(tmp_path: Any):
    # Set up a shell in the temporary directory
    pyshell = PyShell()
    pyshell.cd(tmp_path)

    # Run the command
    branch_name = "foo"
    result = Git.init(branch_name)
    assert result.success
    assert Path(tmp_path, ".git").exists()
