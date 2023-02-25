import os
from pathlib import Path
from pyshell.backends.native_backend import NativeBackend

def test_run_echo():
    cmd = ["echo", "foo"]

    backend = NativeBackend()
    result = backend.run(cmd, Path(os.getcwd()))
    assert result.command == cmd[0]
    assert result.args == cmd[1:]
    assert result.full_command == " ".join(cmd)
    assert result.output == "foo\n"
    assert result.exit_code == 0
    assert result.success
