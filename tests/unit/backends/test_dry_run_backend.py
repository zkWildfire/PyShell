from pyshell.backends.dry_run_backend import DryRunBackend

def test_run_echo():
    cmd = ["echo", "foo"]

    backend = DryRunBackend()
    result = backend.run(cmd)
    assert result.command == cmd[0]
    assert result.args == cmd[1:]
    assert result.full_command == " ".join(cmd)
    assert result.output == ""
    assert result.exit_code == 0
    assert result.success


def test_run_invalid_cmd():
    cmd = ["invalid_cmd"]

    backend = DryRunBackend()
    result = backend.run(cmd)
    assert result.command == cmd[0]
    assert result.args == cmd[1:]
    assert result.full_command == " ".join(cmd)
    assert result.output == ""

    # The dry run backend should assume that all commands succeed
    assert result.exit_code == 0
    assert result.success
