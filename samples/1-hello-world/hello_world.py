#!/usr/bin/env python3
import argparse
from nautilus import Nautilus, AbortOnFailure, BareMetalBackend, \
    SingleFileLogger, MultiFileLogger
from nautilus.shell import Shell

# Decide whether to log to a single file or multiple files
parser = argparse.ArgumentParser()
parser.add_argument("--log", choices=["single", "multi"], default="multi")
args = parser.parse_args()
if args.log == "single":
    logger = SingleFileLogger("hello_world.log", print_cmds=True)
else:
    logger = MultiFileLogger(".logs", print_cmds=True)

# Initialize a Nautilus instance for running commands
# Nautilus commands that don't explicitly specify a Nautilus instance to use
#   will use the default instance.
nautilus = Nautilus(
    BareMetalBackend(),
    logger,
    AbortOnFailure()
)

# Run some commands
Shell.echo("Hello, world!")
Shell.echo("Hello, world again!")
Shell.echo("Howdy, y'all!")
