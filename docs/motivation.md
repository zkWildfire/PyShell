# Motivation
PyShell was born out of a desire to unify platform specific shell scripts into
a single script that would provide a uniform feature set regardless of the OS
a script is executing on. For example, bash offers the `set -e` command to
abort a script as soon as a script command fails:
```sh
#!/usr/bin/env bash
set -e

ls /foo # <<< The script will exit here if /foo doesn't exist
echo "This will not be printed."
```

Batch does not offer an equivalent feature, instead requiring developers to
write multiple extra lines to accomplish the same functionality:
```bat
dir "C:\foo"
if errorlevel 1 (
    exit /b 1
)
```

Using two different shell scripting languages also requires developers to be
familiar with both languages. Even so, it's still extremely easy to
inadvertently introduce small differences in behavior, such as when using the
`echo` command:
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

Standard out of the box python fares better in regards to standardization
between platforms, but suffers when it comes to running commands:
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
!!! warning
    PyShell's CMake module has not been released yet. Also, consider making use
    of PyShell's sibling project, [PyMake](https://www.pymake.dev)! PyMake is to
    CMake as PyShell is to shell scripts.

Unlike the previous python script, the PyShell-based script is much more
strongly typed. When writing the PyShell script, developers don't have to
remember the exact flags that CMake requires for setting its source directory
or build type since IDEs can display the method's parameters to developers.
PyShell will also do additional validation when the script runs, such as
verifying that the CMake executable can be found.
