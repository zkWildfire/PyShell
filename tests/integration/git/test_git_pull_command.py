from pyshell import PyShell
from pyshell.backends.dry_run_backend import DryRunBackend
from pyshell.modules.git import Git

def test_pull_with_no_args():
    backend = DryRunBackend()
    pyshell = PyShell(backend=backend)

    # Run the command
    result = Git.pull(pyshell=pyshell)
    assert result.success
    assert backend.commands == ["git pull"]


def test_pull_from_remote():
    backend = DryRunBackend()
    pyshell = PyShell(backend=backend)

    # Run the command
    remote = "foo"
    result = Git.pull(remote, pyshell=pyshell)
    assert result.success
    assert backend.commands == [f"git pull {remote}"]


def test_pull_from_remote_with_branch_specified():
    backend = DryRunBackend()
    pyshell = PyShell(backend=backend)

    # Run the command
    remote = "foo"
    branch = "bar"
    result = Git.pull(remote, branch, pyshell=pyshell)
    assert result.success
    assert backend.commands == [f"git pull {remote} {branch}"]
