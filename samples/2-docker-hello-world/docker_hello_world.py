#!/usr/bin/env python3
import argparse
import os
from pyshell import PyShell, DockerBackend, KeepGoing, PermitCleanup, \
    NullFileLogger, SingleFileLogger, MultiFileLogger
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

# If this is being run in a dev container or on a CI server, `use_sudo` must be
#   set to True
use_sudo = os.getenv("DEV_CONTAINER") == "1"

# Initialize a PyShell instance for running commands on the host
host_pyshell = PyShell(
    executor=PermitCleanup(),
    error_handler=KeepGoing(),
    logger=logger
)

# Run some commands
Shell.echo("Hello, world!")
Shell.echo("Hello world again!")
Shell.echo("Howdy y'all!")

# Create another PyShell instance that runs commands in a docker container
docker_backend = DockerBackend(host_pyshell, "ubuntu:jammy", use_sudo=use_sudo)
docker_pyshell = PyShell(
    backend=docker_backend,
    logger=logger
)

# Run some commands in the container
Shell.echo("Hello, world!")
Shell.echo("Hello world again!")
Shell.echo("Howdy y'all!")

# Switch back to using the host
host_pyshell.set_as_active_instance()
Shell.echo("Hello, world!")
Shell.echo("Hello world again!")
Shell.echo("Howdy y'all!")

docker_backend.stop()
