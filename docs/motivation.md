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
    build_type=ECMakeBuildType.Debug
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
    PyShell's CMake module has not been released yet.

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

## Logging
PyShell was designed with a heavy emphasis on logging, resulting in a number of
features that assist developers in processing log files generated by a script.
PyShell defaults to only writing information to the console, but its behavior
can be easily adjusted to also write to log files on disk while also printing
to the console. For example, PyShell offers the `SingleFileLogger` and
`MultiFileLogger` classes, which are used in the "Hello World" sample script:
```py title="hello_world.py"
#!/usr/bin/env python3
import argparse
from pyshell import PyShell, NullFileLogger, SingleFileLogger, MultiFileLogger
from pyshell.modules import Shell

# Decide whether to log to a single file or multiple files
parser = argparse.ArgumentParser()
parser.add_argument("--log", choices=["single", "multi"], default=None)
args = parser.parse_args()

if args.log == "single":
    logger = SingleFileLogger("hello_world.log")
elif args.log == "multi":
    logger = MultiFileLogger(
        ".logs",
        print_cmd_header=True,
        print_cmd_footer=True
    )
else:
    logger = NullFileLogger()

# Initialize a PyShell instance for running commands
# PyShell commands that don't explicitly specify a PyShell instance to use
#   will use the default instance.
pyshell = PyShell(logger=logger)

# Run some commands
Shell.echo("Hello, world!")
Shell.echo("Hello world again!")
Shell.echo("Howdy y'all!")
```

When the `NullFileLogger` class is used, the only output from the script is
to the console:
```console
pyshell@85afc3805162:/workspaces/PyShell/samples/1-hello-world$ ./hello_world.py 
Hello, world!
Hello world again!
Howdy y'all!
pyshell@85afc3805162:/workspaces/PyShell/samples/1-hello-world$ ll
total 12
drwxr-xr-x 2 pyshell pyshell 4096 Feb 27 02:55 ./
drwxrwxr-x 3 pyshell pyshell 4096 Feb 23 20:52 ../
-rwxr-xr-x 1 pyshell pyshell  903 Feb 27 02:54 hello_world.py*
```

If the `--log single` flag is provided, output will be written to both the
console and a log file on disk:
```console
pyshell@85afc3805162:/workspaces/PyShell/samples/1-hello-world$ ./hello_world.py --log single
Hello, world!
Hello world again!
Howdy y'all!
pyshell@85afc3805162:/workspaces/PyShell/samples/1-hello-world$ ll
total 16
drwxr-xr-x 2 pyshell pyshell 4096 Feb 27 02:56 ./
drwxrwxr-x 3 pyshell pyshell 4096 Feb 23 20:52 ../
-rw-r--r-- 1 pyshell pyshell   49 Feb 27 02:56 hello_world.log
-rwxr-xr-x 1 pyshell pyshell  903 Feb 27 02:54 hello_world.py*
pyshell@85afc3805162:/workspaces/PyShell/samples/1-hello-world$ cat hello_world.log
Hello, world!

Hello world again!

Howdy y'all!
```

Alternatively, if `--log multi` is used, each command's output is written to its
own file:
```console
pyshell@85afc3805162:/workspaces/PyShell/samples/1-hello-world$ ./hello_world.py --log multi
Hello, world!
Hello world again!
Howdy y'all!
pyshell@85afc3805162:/workspaces/PyShell/samples/1-hello-world$ ll
total 16
drwxr-xr-x 3 pyshell pyshell 4096 Feb 27 02:57 ./
drwxrwxr-x 3 pyshell pyshell 4096 Feb 23 20:52 ../
drwxr-xr-x 2 pyshell pyshell 4096 Feb 27 02:57 .logs/
-rwxr-xr-x 1 pyshell pyshell  903 Feb 27 02:54 hello_world.py*
pyshell@85afc3805162:/workspaces/PyShell/samples/1-hello-world$ ll .logs
total 20
drwxr-xr-x 2 pyshell pyshell 4096 Feb 27 02:57 ./
drwxr-xr-x 3 pyshell pyshell 4096 Feb 27 02:57 ../
-rw-r--r-- 1 pyshell pyshell  306 Feb 27 02:57 1-echo.log
-rw-r--r-- 1 pyshell pyshell  321 Feb 27 02:57 2-echo.log
-rw-r--r-- 1 pyshell pyshell  303 Feb 27 02:57 3-echo.log
pyshell@85afc3805162:/workspaces/PyShell/samples/1-hello-world$ cat .logs/1-echo.log 
[PyShell] Running command: /usr/bin/echo Hello, world!
[PyShell] cwd: /workspaces/PyShell/samples/1-hello-world
[PyShell] Command output:

Hello, world!

[PyShell] Executed command: /usr/bin/echo Hello, world!
[PyShell] cwd: /workspaces/PyShell/samples/1-hello-world
[PyShell] Command exited with code 0.
```

Visible in the multi-file logger example are PyShell's optional header and
footer sections. These sections are enabled by passing these arguments to the
multi-file logger's constructor:
```py
logger = MultiFileLogger(
    ".logs",
    print_cmd_header=True, # <<<
    print_cmd_footer=True  # <<<
)
```
!!! info
    These parameters are also supported by the `SingleFileLogger` class's
    constructor.

PyShell also allows a scanner class to be attached to commands, which enables
PyShell to output extra information to help developers. This is particularly
helpful when dealing with long log files that would otherwise require developers
to scroll through the log to find what they're looking for.

For example, PyShell's `generate_docs.py` script invokes Doxygen and generates
a ~500 line file. Should the command fail, such as due to a parameter lacking
documentation, the `generate_docs.py` script will stop and report an error.
A developer would then need to scroll through the log file generated for the
Doxygen command, find the error message from Doxygen, then open the file and
fix the issue. With PyShell's Doxygen scanner however, the bottom of the log
file contains all the information necessary to fix the issue:
```console title="doxygen.log"
Patching output file 34/36
Patching output file 35/36
Patching output file 36/36
lookup cache used 645/65536 hits=1314 misses=768
finished...
Exiting...

[PyShell] Scanner output:

[PyShell] Missing parameter documentation for:
[PyShell]   File: /workspaces/PyShell/source/pyshell/core/command_metadata.py:15
[PyShell]   Method: pyshell.core.command_metadata.CommandMetadata.__init__(self, str command, Sequence[str] args, CommandFlags flags=CommandFlags.STANDARD, Optional[IScanner] scanner=None)
[PyShell]   Parameter: scanner

[PyShell] Missing parameter documentation for:
[PyShell]   File: /workspaces/PyShell/source/pyshell/doxygen/doxygen_scanner.py:81
[PyShell]   Method: pyshell.doxygen.doxygen_scanner.DoxygenScanner._generate_missing_parameter_entry(self, CommandResult result, str line, List[str] next_lines, int line_number)
[PyShell]   Parameter: result

[PyShell] Executed command: /usr/bin/doxygen /workspaces/PyShell/doxygen/doxyfile
[PyShell] cwd: /workspaces/PyShell
[PyShell] Command exited with code 1.
```

Though scanners are nothing complex, their addition to PyShell is a solid
quality of life addition for developers.
