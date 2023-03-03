## @package pyshell.command
# Contains PyShell command classes.

## @defgroup commands Commands
# Classes that validate and run shell commands and executables.
# PyShell scripts should invoke commands via PyShell `ICommand`-derived classes
#   whenever possible. This allows PyShell to log output from each command and
#   ensures that all errors are handled via the PyShell error handler.
