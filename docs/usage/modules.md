# PyShell Modules
## Overview
PyShell modules are classes that define static methods for constructing and
executing PyShell commands in a single method call. Modules are useful for
organizing commands into logical groups, reducing the number of imports that
need to be added to a script, and to quickly check what commands are available.

For example, the `pyshell.modules.shell` module defines various frequently used
commands, such as `ls`, `cp`, and `rm`. These commands are defined as static
methods, allowing IDEs to suggest them when typing `Shell.`. Additionally, using
the Shell module reduces the number of imports from:
```py
from pyshell.shell.cp_command import CpCommand
from pyshell.shell.echo_command import EchoCommand
from pyshell.shell.ls_command import LsCommand
from pyshell.shell.rm_command import RmCommand

# Set up a PyShell instance
# ...

# Invoke various shell commands
LsCommand('/tmp')()
EchoCommand('Hello, world!')()
RmCommand('/tmp/foo')()
```
To:
```py
from pyshell.modules.shell import Shell

# Set up a PyShell instance
# ...

# Invoke various shell commands
Shell.ls('/tmp')
Shell.echo('Hello, world!')
Shell.rm('/tmp/foo')
```

PyShell currently ships with the following modules:

* [Shell](https://pyshell.dev/doxygen/classpyshell_1_1modules_1_1shell_1_1Shell.html)
* [Doxygen](https://pyshell.dev/doxygen/classpyshell_1_1modules_1_1doxygen_1_1Doxygen.html)
* [Docker](https://pyshell.dev/doxygen/classpyshell_1_1modules_1_1docker_1_1Docker.html)
