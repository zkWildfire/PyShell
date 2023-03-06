# Contributing Guide
## Getting Started
PyShell's repository is set up with support for VSCode's
[devcontainers](https://code.visualstudio.com/docs/devcontainers/containers).
This is the recommended workflow when developing PyShell as it ensures that all
dependencies are installed and configured correctly. If you are not using
VSCode, take a look at the `.devcontainer/ubuntu.dockerfile` file to see what
dependencies are required to develop PyShell. Please note that the
`.devcontainer/devcontainer.json` file also has a few other values that you may
need, such as environment variables that are set within the container.

## General Guidelines
Please keep the following guidelines in mind when contributing to PyShell:

* Type hints must be provided on all methods and variables.

For methods, all method parameters must have type hints. The return value must
have a type hint if it is not `None`. Variables must have type hints if their
type cannot be inferred from the value.

* All code must use Doxygen style comments.

PyShell uses Doxygen to generate its reference documentation. All methods and
parameters must have a Doxygen comment block, and Doxygen is configured to flag
missing documentation as an error. Member variables should have explicit
documentation unless they're directly assigned from constructor parameters, in
which case the constructor parameter documentation will suffice.

For more information on how to use Doxygen and what commands it offers, see the
[Doxygen documentation](https://www.doxygen.nl/manual/index.html).

!!! note
    Although Doxygen is configured to flag missing documentation as an error,
    some documentation elements do not get flagged by Doxygen. For example, it
    is not necessary to add `@returns` to an `@property` method despite it
    technically being a method.

## Adding New Commands
Commands and modules are an area in which contributions are most welcome. Adding
a new command or module is a great way to get started with PyShell development
as it does not require a deep understanding of the internals of PyShell.

To add a new command, you will need to define a new class that inherits from
either `ICommand` or `ExternalCommand`. The `ICommand` class is an abstract base
class that should only be used if the `ExternalCommand` class is unsuitable for
your new custom command. Otherwise, you should use the `ExternalCommand` class
as it provides a lot of functionality that is common to most commands.

You can find the `ICommand` class's definition [here](https://github.com/MYTX-Wildfire/PyShell/blob/master/source/pyshell/commands/command.py)
and the `ExternalClass`'s definition [here](https://github.com/MYTX-Wildfire/PyShell/blob/master/source/pyshell/commands/external_command.py).
The [`ls` command](https://github.com/MYTX-Wildfire/PyShell/blob/master/source/pyshell/shell/ls_command.py)
and [`cp` command](https://github.com/MYTX-Wildfire/PyShell/blob/master/source/pyshell/shell/cp_command.py)
are good examples of how to use the `ExternalCommand` class as a base class.

Here are some guidelines to keep in mind when adding a new command:

* The command's constructor should take a `CommandFlags` parameter.
* Avoid throwing exceptions. Instead, return a `CommandResult` object with the
  `success` property set to `False` when the command is executed. This ensures
  that all commands use the PyShell instance's error handling mechanism.

Following these guidelines will ensure that your command behaves consistently
with other commands.

## Adding New Modules
Once you've implemented a new command(s), it's highly recommended that you also
implement a module for the commands. A module is a loose wrapper around a set of
related commands that allows each command to be executed in a single method call
instead of two method calls. An example of this is the `Shell` module, which
can be found [here](https://github.com/MYTX-Wildfire/PyShell/blob/master/source/pyshell/modules/shell.py).

Here are some guidelines to keep in mind when adding a new module:

* Each method in the module should take the same parameters as the underlying
  command's constructor, plus an additional `PyShell` parameter to be passed to
  the command when executing it. Parameters should be specified in the same
  order in the module as in the command.
