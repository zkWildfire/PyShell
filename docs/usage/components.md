# PyShell Components
## `PyShell` Class
All PyShell-based scripts will need to instantiate one or more instances of the
`PyShell` class. This class acts as a wrapper for the various components that
determine how PyShell executes commands, how the commands' output is logged,
and how errors are handled.

To use the PyShell class, import it using:
```py
from pyshell import PyShell
```

To get started immediately with PyShell, simply instantiate a new instance of
the class:
```py
pyshell = PyShell()
```

A default-constructed PyShell instance will be approximately equivalent to a
bash script that specifies `set -e` at the start of the script. To customize
this behavior, pass different components to the PyShell constructor. For
example, using the `SingleFileLogger` component instead of the default
`ConsoleLogger` component will cause all commands' output to be written to
a file in addition to being displayed in the console's output:
```py
from pyshell import PyShell, SingleFileLogger

pyshell = PyShell(logger=SingleFileLogger("output.log"))
```

Each component that may be passed to the PyShell constructor is documented in
more detail below.

## Backends
PyShell supports three different backends. The `NativeBackend` is the default,
and will run commands on the host machine much like a standard shell script. The
`DryRunBackend` class will print all commands that it would run but will not run
any of the commands. Lastly, the `DockerBackend` will start a docker container
and execute all commands within the docker container.

### Native Backend
The native backend is the default backend and is used when a `PyShell` instance
is instantiated without specifying a backend. The native backend will execute
commands on the host machine.

You can configure a PyShell instance to use the native backend using either of
the following:
```py
from pyshell import PyShell

pyshell = PyShell()
```
```py
from pyshell import PyShell, NativeBackend

pyshell = PyShell(backend=NativeBackend())
```

### Dry Run Backend
The dry run backend will print all commands that it would run but will not run
any of the commands. This is useful for debugging scripts or for testing scripts
without actually running them.

You can configure a PyShell instance to use the dry run backend using:
```py
from pyshell import PyShell, DryRunBackend

pyshell = PyShell(backend=DryRunBackend())
```

### Docker Backend
The docker backend will start a docker container and execute all commands within
the docker container. This is useful for writing scripts that run on a host
machine but need to execute some or all commands within a docker container. To
use the docker backend, you must specify the docker image that you want to use
when instantiating the backend:

```py
from pyshell import PyShell, DockerBackend

backend = DockerBackend("ubuntu:latest")
pyshell = PyShell(backend=backend)

# ...

backend.stop()
```

Note that unlike the other backends, the docker backend must be explicitly
stopped using the `stop()` method. This will ensure that the docker container
is stopped and removed. However, when debugging a script, it may be useful to
comment out the `stop()` call so that you can inspect the docker container after
the script has finished executing.

For more information on how to use the docker backend, see the Docker backend's
documentation, found [here](https://pyshell.dev/doxygen/classpyshell_1_1backends_1_1docker__backend_1_1DockerBackend.html).

## Loggers
Loggers determine how the output of commands are logged. By default, PyShell
uses the `ConsoleLogger` class to log commands' output, which writes all output
to the console. PyShell also ships with several other loggers that may be used
out of the box.

### Console Logger
The console logger is the default logger and is used when a `PyShell` instance
is instantiated without specifying a logger. The console logger will write all
commands' output to the console.

You can configure a PyShell instance to use the console logger using either of
the following:
```py
from pyshell import PyShell

pyshell = PyShell()
```
```py
from pyshell import PyShell, ConsoleLogger

pyshell = PyShell(logger=ConsoleLogger())
```

More information on the console logger can be found in the console logger's
documentation, found [here](https://pyshell.dev/doxygen/classpyshell_1_1logging_1_1console__logger_1_1ConsoleLogger.html).

### Single File Logger
The single file logger will write all commands' output to a single file in
addition to the console. This logger is approximately equivalent to piping all
commands' output to a file using `| tee -a output.log`.

To use the single file logger, you must specify the path to the file that you
want to write to when instantiating the logger:
```py
from pyshell import PyShell, SingleFileLogger

pyshell = PyShell(logger=SingleFileLogger("output.log"))
```

More information on the single file logger can be found in the single file
logger's documentation, found [here](https://pyshell.dev/doxygen/classpyshell_1_1logging_1_1single__file__logger_1_1SingleFileLogger.html).

### Multi File Logger
The multi file logger will write all commands' output to a separate file for
each command. This logger is approximately equivalent to piping each command's
output to a separate file using `| tee cmd.log`. Using the multi file logger
has multiple benefits over emulating the same behavior using `tee`; for example,
the multi file logger will automatically create a new file for each command
and will automatically assign the file a name based on the command's name and
number of commands that have been run. For example, if a script runs `echo`,
then `rm`, then `ls`, the logger will create three files:

* `1-echo.log` - contains the output of the `echo` command
* `2-rm.log` - contains the output of the `rm` command
* `3-ls.log` - contains the output of the `ls` command

To use the multi file logger, you must specify the path to the directory that
you want to write the files to when instantiating the logger:
```py
from pyshell import PyShell, MultiFileLogger

pyshell = PyShell(logger=MultiFileLogger("logs"))
```

More information on the multi file logger can be found in the multi file
logger's documentation, found [here](https://pyshell.dev/doxygen/classpyshell_1_1logging_1_1multi__file__logger_1_1MultiFileLogger.html).

### Null Logger
The null logger will not log any commands' output and is equivalent to piping
all commands' output to `/dev/null`.

You can configure a PyShell instance to use the null logger using:
```py
from pyshell import PyShell, NullLogger

pyshell = PyShell(logger=NullLogger())
```

More information on the null logger can be found in the null logger's
documentation, found [here](https://pyshell.dev/doxygen/classpyshell_1_1logging_1_1null__logger_1_1NullLogger.html).

## Executors
PyShell's executor component determines whether a command is allowed to execute.
By default, PyShell uses the `AllowAll` executor, which allows all non-inactive
commands to be run. PyShell also ships with a `PermitCleanup` executor that
blocks execution of non-cleanup commands after a failure has occurred.

### Allow All Executor
The allow all executor is the default executor and is used when a `PyShell`
instance is instantiated without specifying an executor. The allow all executor
will allow all non-inactive commands to be run regardless of whether a failure
has occurred.

You can configure a PyShell instance to use the allow all executor using either
of the following:
```py
from pyshell import PyShell

pyshell = PyShell()
```
```py
from pyshell import PyShell, AllowAll

pyshell = PyShell(executor=AllowAll())
```

More information on the allow all executor can be found in the allow all
executor's documentation, found [here](https://pyshell.dev/doxygen/classpyshell_1_1executors_1_1allow__all_1_1AllowAll.html).

### Permit Cleanup Executor
The permit cleanup executor will block execution of non-cleanup commands after a
failure has occurred. This executor is useful for writing scripts that need to
perform cleanup tasks after a failure has occurred. For example, if a script
needs to remove a file after a failure has occurred, the script can use the
permit cleanup executor to ensure that the file is removed even if the script
fails.

To use the permit cleanup executor, you must specify the path to the file that
you want to write to when instantiating the logger:
```py
from pyshell import PyShell, PermitCleanup

pyshell = PyShell(executor=PermitCleanup())
```

More information on the permit cleanup executor can be found in the permit
cleanup executor's documentation, found [here](https://pyshell.dev/doxygen/classpyshell_1_1executors_1_1permit__cleanup_1_1PermitCleanup.html).

## Error Handlers
PyShell's error handler component determines how a command's failure is handled.
Error handlers are closely related to executors; the difference is that error
handlers are called after a command has failed, whereas executors are called
before a command is run. By default, PyShell uses the `AbortOnFailure` error
handler, which will abort the script if a command fails. PyShell also ships with
a `KeepGoing` error handler that will continue executing the script after a
command has failed.

### Abort On Failure Error Handler
The abort on failure error handler is the default error handler and is used when
a `PyShell` instance is instantiated without specifying an error handler. The
abort on failure error handler will cause a script to be immediately aborted if
a command fails. This error handler is equivalent to using the `set -e` option
in bash.

You can configure a PyShell instance to use the abort on failure error handler
using either of the following:
```py
from pyshell import PyShell

pyshell = PyShell()
```
```py
from pyshell import PyShell, AbortOnFailure

pyshell = PyShell(error_handler=AbortOnFailure())
```

More information on the abort on failure error handler can be found in the abort
on failure error handler's documentation, found [here](https://pyshell.dev/doxygen/classpyshell_1_1error_1_1abort__on__failure_1_1AbortOnFailure.html).

### Keep Going Error Handler
The keep going error handler will continue executing the script after a command
has failed. This error handler is equivalent to using the `set +e` option in
bash. This error handler is useful for writing scripts that need to continue
executing after a command has failed and is frequently used with the permit
cleanup executor.

You can configure a PyShell instance to use the keep going error handler using
the following:
```py
from pyshell import PyShell, KeepGoing

pyshell = PyShell(error_handler=KeepGoing())
```

More information on the keep going error handler can be found in the keep going
error handler's documentation, found [here](https://pyshell.dev/doxygen/classpyshell_1_1error_1_1keep__going_1_1KeepGoing.html).

## Configuration
PyShell also allows values to be specified for built in options. These options
may be queried by PyShell commands to determine how they should behave. For
example, you can enable verbose logging by setting the `verbose` option to
`True`:
```py
from pyshell import PyShell, PyShellOptions

pyshell = PyShell(options=PyShellOptions(verbose=True))
```

Commands that support verbose output will check the shell's `verbose` option
and enable verbose output if the option is set to `True`.

More information on the built in options can be found in the `PyShellOptions`
documentation, found [here](https://pyshell.dev/doxygen/classpyshell_1_1core_1_1pyshell__options_1_1PyShellOptions.html).
