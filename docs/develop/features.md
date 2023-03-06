## PyShell Features
* Cross platform support

!!! warning
    PyShell is currently only tested on Linux and a few of the shell commands
    are not yet cross platform. This will be updated in the near future since
    PyShell will be used in projects that need to run on Windows.

PyShell scripts are standard python scripts and can be run on any platform that
Python supports. Built-in PyShell modules are designed to be cross platform,
so PyShell-based scripts generally do not need to branch by OS. By writing
scripts using PyShell, you'll no longer need to write bash and batch scripts
that are functionally identical.

* Command autocompletion

The built-in PyShell modules allow shell commands and external executables to
be invoked as Python methods. This allows IDEs to present information about the
parameters that the method accepts instead of forcing developers to try and
remember exactly what flag it was that does what you need.

* Automatic logging to files

Using PyShell's built in logger classes, you can choose how you want to log your
script's output. For example, you can configure PyShell to tee all output from
commands executed by your script to a single file, or you can choose to write
each command's output to a different file. Logging configuration is handled when
you initialize a `PyShell` class instance and does not need to be handled on a
per-command basis.

* Error handling

PyShell gives scripts a lot of control over how they want to handle errors.
Basic scripts may simply want to abort script execution upon encountering an
error, while other scripts may want to continue executing certain commands such
as cleanup commands. PyShell provides built-in classes that make it easy to
implement proper error handling in scripts.

* Automatic validation

It's all too easy to write scripts that assume certain conditions are true and
end up erroring out far away from where the invalid assumption is located.
PyShell commands automatically validate their input and any external state
required to run the command when the command instance is constructed, allowing
errors to be detected as early as possible.

* Docker container support

PyShell instances can be configured to target a docker container instead of
running commands on the host system. This means that a PyShell script can
execute commands on the host system as well as within a docker container -
all from a single script and with a non-branching code path.
