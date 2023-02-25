## @package pyshell.core
# Contains PyShell core classes.

## @defgroup commands Commands
# Classes that validate and run shell commands and executables.
# PyShell scripts should invoke commands via PyShell `ICommand`-derived classes
#   whenever possible. This allows PyShell to log output from each command and
#   ensures that all errors are handled via the PyShell error handler.

## @defgroup modules Modules
# Modules allow easier access to PyShell commands.
# Modules allow PyShell commands to be invoked via a single function call rather
#   than constructing a PyShell command instance and then executing it. For
#   PyShell scripts that don't need advanced PyShell features like parallel
#   execution, modules are the recommended way to invoke PyShell commands.
