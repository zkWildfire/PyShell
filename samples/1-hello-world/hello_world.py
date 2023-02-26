#!/usr/bin/env python3
import argparse
from pyshell import PyShell, PyShellOptions, AbortOnFailure, AllowAll, \
    NativeBackend, SingleFileLogger, MultiFileLogger
from pyshell.modules import Shell

# Decide whether to log to a single file or multiple files
parser = argparse.ArgumentParser()
parser.add_argument("--log", choices=["single", "multi"], default="multi")
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()
if args.log == "single":
    logger = SingleFileLogger("hello_world.log")
else:
    logger = MultiFileLogger(
        ".logs",
        print_cmd_header=True,
        print_cmd_footer=True
    )

# Initialize a PyShell instance for running commands
# PyShell commands that don't explicitly specify a PyShell instance to use
#   will use the default instance.
pyshell = PyShell(
    NativeBackend(),
    logger,
    AllowAll(),
    AbortOnFailure(),
    PyShellOptions(
        verbose=args.verbose
    )
)

# Run some commands
Shell.echo("Hello, world!")
Shell.echo("Hello world again!")
Shell.echo("Howdy y'all!")
