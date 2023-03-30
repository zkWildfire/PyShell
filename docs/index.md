# PyShell
## What is PyShell?
PyShell is a Python library designed to help developers create shell scripts.
At its most basic, PyShell can be thought of as a wrapper around
`subprocess.run()` that allows IDEs to display autocompletion help for commands.
However, PyShell is much more than a basic wrapper and offers many features that
greatly improve development workflows.

## Getting Started
- Looking to use PyShell to write your own shell scripts? Take a look at
  PyShell's [Sample Scripts](learn/sample-scripts.md) and learn about PyShell's
  components via the Usage section of PyShell's docs.
- Want to know what PyShell is capable of? Check out the [Features](develop/features.md)
  page.
- Wondering why PyShell was created? The [Motivation](motivation.md) page
  explains the reasoning behind PyShell's design.
- Interested in contributing to PyShell? Read PyShell's
  [Contributing Guide](develop/contributing.md) and the Develop section of
  PyShell's docs.

## Features
* Cross platform support\*
* Command autocompletion
* Automatic logging to files
* Error handling
* Automatic validation
* Asynchronous commands
* Docker container support

\* As a Python library, PyShell is inherently cross platform. However, PyShell
is currently only tested on Linux and a few of the shell commands invoke unix
commands. If running on Windows, the current recommendation is to have Git for
Windows installed and have its `bin` directory added to your `PATH`. This will
ensure that all PyShell commands function as expected.

## Installation
Currently, PyShell is **not** available on PyPI. To install PyShell, clone the
repository or add it as a submodule, then configure your `PYTHONPATH` to include
the `source` directory in the PyShell repository. PyShell will be added to PyPI
once it is ready for a stable release.

## Platform Support
PyShell is designed to be cross platform and will be usable on Linux, Windows,
and macOS. However, PyShell has only been tested on Linux so far and requires a
few changes before it will be usable on Windows. Support for Windows will be
added in a future release as PyShell is developed further.

## License
PyShell is licensed under the MIT license.
