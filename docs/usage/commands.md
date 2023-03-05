# PyShell Commands
## Overview
PyShell commands are classes that execute a specific task. Most PyShell commands
map one to one with a command line tool, though this is not a requirement. All
commands execute by invoking an external command or executable, which allows
PyShell to capture the command's output and log it using the PyShell instance's
configured logger. PyShell commands may also perform extra validation and error
handling, such as checking for the existence of a required executable.

## General Usage
For most scripts, commands will be invoked via [modules](modules.md). However,
commands may also be explicitly constructed and invoked, which allows a
command's invocation to be separate from where it is defined.

In general, command classes will define constructor parameters corresponding
to the most command command flags and options. These parameters are used to
construct the command's command line arguments. For example, the `ls` command
defines an optional `target_path` parameter, which is passed to `ls` if it's
provided:
```py
from pyshell.shell.ls_command import LsCommand

# Set up a PyShell instance
# ...

# Invoke `ls` with no arguments
cmd1 = LsCommand()
cmd1()

# Invoke `ls` with the argument `/tmp`
cmd2 = LsCommand('/tmp')
cmd2()

# Invoke `ls` with the argument `/home`
cmd3 = LsCommand(target_path='/home')
cmd3()
```

The purpose of commands is to provide stricter type checking for command
parameters and to enable IDEs to suggest parameters that may be passed to a
command. This is especially evident when using Docker commands, which frequently
require a large number of parameters. For example, the `docker run` command
accepts more than 10 parameters in its constructor. Rather than needing to
remember whether specifying ports is done using `--ports` or `--publish`, a
developer simply needs to look at their IDE's suggestions for the run command's
constructor. Each constructor parameter is also strongly typed where possible,
reducing the likelihood of a developer passing an invalid value.

## Flags
PyShell-specific flags may be specified when constructing a command, which is
passed in via the `cmd_flags` parameter for most command classes. These flags
are most frequently used to prevent a command from executing by marking it as
inactive, ensuring that a command is always run by marking it as a cleanup
command, or to modify how the command's output is logged. The full set of flags
can be found [here](https://pyshell.dev/doxygen/classpyshell_1_1commands_1_1command__flags_1_1CommandFlags.html).

Command flags may also be dynamically set using a custom condition or by
checking if another command has failed. For example, the following command
will only execute if the `ls` command fails:
```py
from pyshell import enable_if
from pyshell.shell.ls_command import LsCommand

# Set up a PyShell instance
# ...

# Invoke the `ls` command; assume that it fails
result = LsCommand()()

# Invoke the `echo` command, but only if the `ls` command failed
cmd = EchoCommand('Hello, world!', cmd_flags=enable_if(result.failed))
cmd()
```

More information on the `enable_if` function can be found [here](https://pyshell.dev/doxygen/group__commands.html#gafb2cb15f989412bc7fd0dabb6a38a587).

## Custom Commands
There are an infinite number of commands that may be executed by a shell script,
and commands frequently offer a large number of flags. While PyShell provides
a large number of commands out of the box, it is not possible to provide a
command for every possible use case. To address this, PyShell provides an
`ExternalCommand` class that may be used directly from within a PyShell script
to execute a command while still taking advantage of PyShell's logging and error
handling.

The `ExternalCommand` class may be used like this:
```py
from pyshell.commands.external_command import ExternalCommand

# Set up a PyShell instance
# ...

# Invoke `ls` with no arguments
cmd1 = ExternalCommand('ls')
cmd1()

# Invoke `ls` with the argument `/tmp`
cmd2 = ExternalCommand('ls', '/tmp')
cmd2()

# Invoke `ls` with the argument `/tmp` and the flag `--all`
cmd3 = ExternalCommand('ls', ['/tmp', '--all'])
cmd3()

# Invoke `ls` and silence its output
cmd4 = ExternalCommand('ls', cmd_flags=CommandFlags.QUIET)
cmd4()
```
