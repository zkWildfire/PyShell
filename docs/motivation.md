# Motivation
## Shell Scripts
PyShell was born out of a desire to unify platform specific shell scripts into
a single script with a uniform feature set regardless of OS. For example, bash
offers the `set -e` command to abort a script as soon as a script command fails:
```sh title="error.sh"
#!/usr/bin/env bash
set -e

ls /foo # <<< The script will exit here if /foo doesn't exist
echo "This will not be printed."
```

But Batch does not offer an equivalent feature, instead requiring developers to
write multiple extra lines to accomplish the same functionality:
```bat title="error.bat"
dir "C:\foo"
if errorlevel 1 (
    exit /b 1
)
```

Using two different shell scripting languages also requires developers to be
familiar with both languages. Even so, it's extremely easy to inadvertently
introduce small differences in behavior, such as when using the `echo` command:
```sh title="echo.sh"
#!/usr/bin/env bash
echo "foo"

# Output:
foo
```
```bat title="echo.bat"
@echo off
echo "foo"

REM Output:
"foo"
```

Standard out-of-the-box python fares better in regards to standardization
between platforms, but suffers when running commands:
```sh title="cmake.sh"
#!/usr/bin/env bash
set -e

# Run CMake's configure step
cmake -S . -B _build -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=_out

# Build the project
cmake --build _build --target install
```
```bat title="cmake.bat"
@echo off

REM Run CMake's configure step
cmake.exe -S . -B _build -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=_out
if errorlevel 1 (
    exit /b
)

REM Build the project
cmake.exe --build _build --target install
if errorlevel 1 (
    exit /b
)
```
```py title="cmake.py"
#!/usr/bin/env python3
import subprocess

# Run CMake's configure step
subprocess.run(
    [
        "cmake",
        "-S",
        ".",
        "-B",
        "_build",
        "-DCMAKE_BUILD_TYPE=Debug",
        "-DCMAKE_INSTALL_PREFIX=_out"
    ],
    check=True
)

# Run CMake's build step
subprocess.run(
    ["cmake", "--build", "_build", "--target", "install"],
    check=True
)
```

This is where PyShell and its built in modules come into play. Using PyShell's
CMake module, that `cmake.py` script could be written this way instead:
```py title="cmake.py"
from pyshell import PyShell, AbortOnFailure
from pyshell.modules import CMake, ECMakeBuildType

pyshell = PyShell(error_handler=AbortOnFailure())

# Named function arguments shown for clarity only
CMake.configure(
    source=".",
    build="_build",
    install="_out",
    build_type=ECMakeBuildType.Debug,
)
CMake.build(
    build="_build",
    target="install"
)
```
Without the named function arguments, the script is almost on par with the
bash script:
```py title="cmake.py"
from pyshell import PyShell, AbortOnFailure
from pyshell.modules import CMake, ECMakeBuildType

pyshell = PyShell(error_handler=AbortOnFailure())

# Run CMake's configure step
CMake.configure(".", "_build", "_out", ECMakeBuildType.Debug)

# Run CMake's build step
CMake.build("_build", "install")
```

!!! warning
    PyShell's CMake module has not been released yet. You may also want to
    consider making use of PyShell's sibling project, [PyMake](https://www.pymake.dev)!
    PyMake is to CMake as PyShell is to shell scripts.

Unlike the previous python script, the PyShell-based script is much more
strongly typed. When writing the PyShell script, developers don't have to
remember the exact flags that CMake requires for setting its source directory
or build type since IDEs can display the method's parameters to developers.
PyShell will also do additional validation when the script runs, such as
verifying that the CMake executable can be found.

## Error Handling
Though PyShell's foundation was rooted in using Python for shell scripts,
PyShell has grown into much more. PyShell shines particularly bright when it
comes to error handling, where PyShell scripts have significant improvements
over their batch/bash counterparts.

For example, consider this bash script:
```sh title="error.sh"
#!/usr/bin/env bash
set -e

echo "before failed command"
ls /foo/bar
echo "after failed command"
echo "perform cleanup"
```

The output of that script is:
```console
pyshell@85afc3805162:/workspaces/PyShell$ ./error.sh
before failed command
ls: cannot access '/foo/bar': No such file or directory
```

This script is just a toy script, but imagine if the script's cleanup command
had to run something more important. What if the cleanup command was one that
corrected file permissions on a CI/CD system, and now every subsequent CI/CD
run on that machine will now fail? That's obviously no good, so the script
clearly must be adjusted to handle that. There's more than one way to go about
this, such as:
```sh title="error.sh"
#!/usr/bin/env bash
set -e

echo "before failed command"

if ! ls /foo/bar; then
    echo "error"
fi

echo "after failed command"
echo "perform cleanup"
```

The updated script's output:
```console
pyshell@85afc3805162:/workspaces/PyShell$ ./error.sh
before failed command
ls: cannot access '/foo/bar': No such file or directory
error
after failed command
perform cleanup
```

This is better, but now there's a different problem. If the "after failed
command" command is only valid to be executed if the failing command finished
successfully, then now the script will now terminate on that line instead.
That command could be moved into the if statement, but a real script may have
many lines between the two commands or many dependent commands. Alternatively,
the cleanup code could be moved into its own function:
```sh title="error.sh"
#!/usr/bin/env bash
set -e

cleanup() {
    echo "perform cleanup"
    exit $1
}

echo "before failed command"
ls /foo/bar || cleanup 1
echo "after failed command" || cleanup 1
cleanup 0
```

Output:
```console
pyshell@85afc3805162:/workspaces/PyShell$ ./error.sh
before failed command
ls: cannot access '/foo/bar': No such file or directory
perform cleanup
```

That's a significant improvement, but PyShell can do even better:
```py title="error.py"
#!/usr/bin/env python3
from pyshell import PyShell, KeepGoing, PermitCleanup, CommandFlags
from pyshell.modules import Shell

pyshell = PyShell(
    executor=PermitCleanup(),
    error_handler=KeepGoing()
)

# No commands have failed, so this command will be run
Shell.echo("before failed command")

# This command will fail, but the error handler will ignore it because the
#   error handler is set to `KeepGoing`
Shell.ls("/foo/bar")

# This command won't run because it's a standard command
Shell.echo("after failed command")

# This command will run because it's a cleanup command
Shell.echo("perform cleanup", cmd_flags=CommandFlags.CLEANUP)
```

Output:
```console
pyshell@85afc3805162:/workspaces/PyShell$ ./sample.py
before failed command
/usr/bin/ls: cannot access '/foo/bar': No such file or directory
Command '/usr/bin/ls' failed with exit code 2.
Note: Full command was '/usr/bin/ls /foo/bar'.
perform cleanup
```

This example introduces a new PyShell concept, the executor. This is a component
that decides whether a command is allowed to execute. In this example, the
`PermitCleanup` executor is used along with the `KeepGoing` error handler. This
is necessary to avoid stopping the script immediately upon a command failing,
which is what would happen if the script had used the `AbortOnFailure` error
handler. The `KeepGoing` error handler also isn't usable on its own in this
scenario, as otherwise it would allow the "after failed command" echo command
to be executed.

Instead, the combination of the `PermitCleanup` executor and the `KeepGoing`
error handler ensures that all commands after the failed command do not
execute... *except* cleanup commands. By using these two PyShell components,
the script can be written with a linear structure that does not require the
reader to jump to the cleanup method to discover what the script runs.
