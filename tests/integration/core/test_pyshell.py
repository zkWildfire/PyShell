from pathlib import Path
from pyshell.core.pyshell import PyShell
from pyshell.core.pyshell_options import PyShellOptions
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
    Shell.ls(Path.joinpath(tmp_path, "foo"), pyshell=pyshell)

    # This command should be skipped by the executor
    result = Shell.ls()
    assert result.skipped


def test_print_normal_verbosity_message():
    output = ""
    def print_func(*messages: object, **kwargs: Any):
        nonlocal output
        for m in messages:
            output += str(m)

    pyshell = PyShell()
    msg = "foo"
    pyshell.print(msg, print_func=print_func)

    assert output == msg


def test_print_high_verbosity_message():
    output = ""
    def print_func(*messages: object, **kwargs: Any):
        nonlocal output
        for m in messages:
            output += str(m)

    verbosity_level = 1
    pyshell = PyShell(
        options=PyShellOptions(
            verbose=verbosity_level
        )
    )
    msg = "foo"
    pyshell.print(msg, verbose=True, print_func=print_func)

    assert output == msg


def test_skip_printing_high_verbosity_message():
    output = ""
    def print_func(*messages: object, **kwargs: Any):
        nonlocal output
        for m in messages:
            output += str(m)

    verbosity_level = 1
    pyshell = PyShell(
        options=PyShellOptions(
            verbose=verbosity_level
        )
    )
    msg = "foo"
    pyshell.print(msg, verbose=verbosity_level+1, print_func=print_func)

    assert output == ""


def test_quiet_mode_disables_verbose_output():
    output = ""
    def print_func(*messages: object, **kwargs: Any):
        nonlocal output
        for m in messages:
            output += str(m)

    verbosity_level = 1
    pyshell = PyShell(
        options=PyShellOptions(
            verbose=verbosity_level,
            quiet=True
        )
    )
    msg = "foo"
    pyshell.print(msg, verbose=verbosity_level, print_func=print_func)

    assert output == ""


def test_quiet_mode_disables_normal_output():
    output = ""
    def print_func(*messages: object, **kwargs: Any):
        nonlocal output
        for m in messages:
            output += str(m)

    pyshell = PyShell(
        options=PyShellOptions(
            quiet=True
        )
    )
    msg = "foo"
    pyshell.print(msg, print_func=print_func)

    assert output == ""
