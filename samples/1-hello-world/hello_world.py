#!/usr/bin/env python3
from nautilus import Nautilus, AbortOnFailure, SingleFileLogger, MultiFileLogger, BareMetalBackend
from nautilus.shell import Shell

nautilus = Nautilus(
    BareMetalBackend(),
    # SingleFileLogger("hello_world.log"),
    MultiFileLogger(".logs"),
    AbortOnFailure()
)
Shell.echo("Hello, world!")
Shell.echo("Hello, world again!")
Shell.echo("Howdy, y'all!")
