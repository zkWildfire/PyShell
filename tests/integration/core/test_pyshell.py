from pathlib import Path
from pyshell.core.pyshell import PyShell
from pyshell.error.keep_going import KeepGoing
from pyshell.executors.permit_cleanup import PermitCleanup
from pyshell.modules.shell import Shell
from pyshell.shell.ls_command import LsCommand
from typing import Any

def test_run_in_custom_absolute_cwd():
    pyshell = PyShell()
    cmd = LsCommand()
    cwd = "/"
    result = cmd(pyshell, cwd)

    assert result.success
    assert result.cwd == cwd


def test_run_in_custom_relative_cwd():
    pyshell = PyShell()
    cmd = LsCommand()
    cwd = ".."
    result = cmd(pyshell, cwd)

    assert result.success
    assert result.cwd == str(Path.cwd().joinpath(cwd).resolve())


def test_cmd_runs_in_pyshell_cwd_by_default():
    pyshell = PyShell()
    cmd = LsCommand()
    result = cmd(pyshell)

    assert result.success
    assert result.cwd == str(pyshell.cwd)


def test_skip_cmd_via_executor(tmp_path: Any):
    pyshell = PyShell(
        executor=PermitCleanup(),
        error_handler=KeepGoing()
    )

    # Run a command that will fail
    Shell.ls(Path.joinpath(tmp_path, "foo"), pyshell)

    # This command should be skipped by the executor
    result = Shell.ls()
    assert result.skipped
