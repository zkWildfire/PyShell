# Sample Scripts
## Overview
Several sample scripts are provided as part of the PyShell repository to
demonstrate the use of the PyShell framework. These scripts are located in the
`samples` directory of the repository. For more information on each script,
see below.

## 1. `hello_world.py`
This script demonstrates the basic usage of the PyShell framework. It
implements a simple shell that prints several messages using the `Shell`
module's `echo()` method, then exits. The script can be found [here](https://github.com/MYTX-Wildfire/PyShell/blob/master/samples/1-hello-world/hello_world.py).

This script may be invoked with no arguments, which will cause the script to
print its messages to the console. Alternatively, the script may be invoked
with the argument `--log single` or `--log multi`, which will cause the script
to print its messages to a single log file or multiple log files, respectively.
The script also supports three verbosity levels, which determine whether no
extra output is printed, only command headers are printed, or command headers
and footers are printed. By default, no extra output is printed. Printing
command headers can be enabled by passing `-v` or `--verbose` as an argument,
while printing command footers can be enabled by passing `-vv` or by passing
`--verbose` twice.

## 2. `docker_hello_world.py`
This script demonstrates the use of the PyShell framework to execute Docker
commands. It first prints multiple commands on the host using the `Shell`
module's `echo()` method, then starts a docker container. The messages are then
repeated inside the container, then the container is stopped and removed.
Lastly, the script repeats the commands on the host again. The script can be
found [here](https://github.com/MYTX-Wildfire/PyShell/blob/master/samples/2-docker-hello-world/docker_hello_world.py).

This script supports the same arguments as the `hello_world.py` script.
