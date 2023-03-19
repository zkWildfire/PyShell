from pathlib import Path
from pyshell import PyShell, KeepGoing
from pyshell.modules.git import Git
from typing import Any

def test_switch_to_existing_branch(tmp_path: Any):
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

    # Create a new branch
    branch_name = "foo"
    result = Git.branch(branch_name, create_branch=True)
    assert result.success

    # Switch to the new branch
    result = Git.switch(branch_name)
    assert result.success

    # Make sure the branch was switched to
    result = Git.status()
    assert result.success
    assert branch_name in result.output


def test_switch_to_non_existing_branch(tmp_path: Any):
    # Set up a shell in the temporary directory
    pyshell = PyShell(error_handler=KeepGoing())
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

    # Switch to a non-existing branch
    branch_name = "foo"
    result = Git.switch(branch_name)
    assert not result.success

    # Make sure the branch was not switched to
    result = Git.status()
    assert result.success
    assert initial_branch in result.output


def test_switch_to_non_existing_branch_with_create(tmp_path: Any):
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

    # Switch to a non-existing branch
    branch_name = "foo"
    result = Git.switch(branch_name, create_branch=True)
    assert result.success

    # Make sure the branch was switched to
    result = Git.status()
    assert result.success
    assert branch_name in result.output
