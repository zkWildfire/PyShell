#!/usr/bin/env python3
import argparse
from pathlib import Path
from pyshell import PyShell, AbortOnFailure, NativeBackend, MultiFileLogger
from pyshell.modules import Doxygen, Shell

# Process arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "--clean",
    action="store_true",
    help="Delete the output directory before generating new files."
)
parser.add_argument(
    "--publish",
    action="store_true",
    help="Publish the generated documentation to GitHub Pages."
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Enable verbose logging."
)
parser.add_argument(
    "--output",
    default=".docs",
    help="The output directory for the generated documentation."
)
args = parser.parse_args()

# Validate arguments
output_path = Path(args.output).resolve()
if output_path.is_file():
    raise ValueError(f"'{output_path}' is a file.")

# Initialize a PyShell instance for running commands
pyshell = PyShell(
    NativeBackend(),
    MultiFileLogger(".logs", print_cmds=True),
    AbortOnFailure()
)

# If the --clean flag was specified, delete the docs directory
if args.clean:
    Shell.rm(output_path)

# Generate the documentation
DOXYFILE_PATH = Path(__file__).parent.joinpath("doxygen", "doxyfile")
Doxygen.generate_docs(DOXYFILE_PATH)
