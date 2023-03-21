# Roadmap
!!! warning
    All features listed here are subject to change. Features will be implemented
    on an as-needed basis to support other projects.

* Windows support

This will be the next feature to be implemented. PyShell is intended to be cross
platform, but a few of the shell commands need to be updated to invoke the
correct Windows commands instead of assuming that the host system is Linux.
Also, PyShell's CI/CD pipeline will need to be updated to run tests on Windows.

* SSH support

PyShell is already capable of running commands on a not-host machine by way of
invoking commands in a docker container. An `SshBackend` class will be added in
the future to allow PyShell to run commands on a remote machine via SSH.

* MultiSSH support

A new `PyShell`-style class will be added that allows commands to be run on
multiple targets at the same time. This will be used to implement a
`MultiSshBackend` that allows the same commands to be run on multiple remote
machines at the same time.

* Per-invocation overrides

With PyShell's split between when a command is defined and when it is invoked,
it would be possible to add support for overriding components or parameters when
a command is invoked. This would allow a command to be defined once and then
reused with different parameters or components; for example, a PyShell instance
could be configured to use the `ConsoleLogger` class, but a singular command
in the script could be configured to use the `SingleFileLogger` class instead.
