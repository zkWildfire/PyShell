#!/usr/bin/env python3
import argparse
from pyshell import PyShell, AbortOnFailure, BareMetalBackend, \
    SingleFileLogger, MultiFileLogger
from pyshell.shell import Shell

# Decide whether to log to a single file or multiple files
parser = argparse.ArgumentParser()
parser.add_argument("--log", choices=["single", "multi"], default="multi")
args = parser.parse_args()
if args.log == "single":
    logger = SingleFileLogger("hello_world.log", print_cmds=True)
else:
    logger = MultiFileLogger(".logs", print_cmds=True)

# Initialize a PyShell instance for running commands
# PyShell commands that don't explicitly specify a PyShell instance to use
#   will use the default instance.
pyshell = PyShell(
    BareMetalBackend(),
    logger,
    AbortOnFailure()
)

# Run some commands
Shell.echo("Hello, world!")
Shell.echo("Hello, world again!")
Shell.echo("Howdy, y'all!")
