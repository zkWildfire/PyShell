from pathlib import Path
from pyshell import PyShell
from pyshell.modules.git import Git
from typing import Any

def test_print_current_branch(tmp_path: Any):
    # Set up a shell in the temporary directory
    pyshell = PyShell()
    pyshell.cd(tmp_path)

    # Set up the repository
    branch_name = "foobar"
    result = Git.init(branch_name)
    assert result.success
    path = Path(tmp_path, "foo.txt")
    path.write_text("foo bar")
    result = Git.add(path)
    assert result.success
    result = Git.commit("Initial commit")
    assert result.success

    # Run the command
    result = Git.status()
    assert result.success
    assert branch_name in result.output


def test_create_branch(tmp_path: Any):
    # Set up a shell in the temporary directory
    pyshell = PyShell()
    pyshell.cd(tmp_path)

    # Set up the repository
    initial_branch = "master"
    result = Git.init(initial_branch)
    assert result.success
    path = Path(tmp_path, "foo.txt")
    path.write_text("foo bar")
    result = Git.add(path)
    assert result.success
    result = Git.commit("Initial commit")
    assert result.success

    # Run the command
    branch_name = "foo"
    result = Git.branch(branch_name, create_branch=True)
    assert result.success

    result = Git.branch()
    assert result.success
    assert branch_name in result.output

    # Make sure the branch was created but not switched to
    result = Git.status()
    assert result.success
    assert initial_branch in result.output
