from pyshell import PyShell
from pyshell.backends.dry_run_backend import DryRunBackend
from pyshell.modules.git import Git

def test_push_with_no_args():
    backend = DryRunBackend()
    pyshell = PyShell(backend=backend)

    # Run the command
    result = Git.push(pyshell=pyshell)
    assert result.success
    assert backend.commands == ["git push"]


def test_push_from_remote():
    backend = DryRunBackend()
    pyshell = PyShell(backend=backend)

    # Run the command
    remote = "foo"
    result = Git.push(remote, pyshell=pyshell)
    assert result.success
    assert backend.commands == [f"git push {remote}"]
