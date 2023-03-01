#!/usr/bin/env python3
import argparse
from pyshell import PyShell, NullFileLogger, SingleFileLogger, MultiFileLogger
from pyshell.modules import Shell

# Decide whether to log to a single file or multiple files
parser = argparse.ArgumentParser()
parser.add_argument("--log", choices=["single", "multi"], default=None)
parser.add_argument("-v", "--verbose", action="count")
args = parser.parse_args()

if args.log == "single":
    logger = SingleFileLogger(
        "hello_world.log",
        print_cmd_header=args.verbose > 0,
        print_cmd_footer=args.verbose > 1
    )
elif args.log == "multi":
    logger = MultiFileLogger(
        ".logs",
        print_cmd_header=args.verbose > 0,
        print_cmd_footer=args.verbose > 1
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
