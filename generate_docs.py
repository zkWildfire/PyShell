#!/usr/bin/env python3
import argparse
from pathlib import Path
from pyshell import PyShell, AbortOnFailure, NativeBackend, MultiFileLogger
from pyshell.modules import Doxygen, Moxygen, Shell

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

# Constants
LOGS_DIR = ".logs"
SCRIPT_DIR = Path(__file__).parent
DOXYFILE_PATH = SCRIPT_DIR.joinpath("doxygen", "doxyfile")
DOCS_DIR = SCRIPT_DIR.joinpath(".docs")
DOXYGEN_XML_PATH = DOCS_DIR.joinpath("xml")
MOXYGEN_MD_PATH = DOCS_DIR.joinpath("md")

# Initialize a PyShell instance for running commands
pyshell = PyShell(
    NativeBackend(),
    MultiFileLogger(LOGS_DIR, print_cmds=True),
    AbortOnFailure()
)

# If the --clean flag was specified, delete generated directories
if args.clean:
    Shell.rm(LOGS_DIR, force=True)
    Shell.rm(DOCS_DIR, force=True)
    Shell.rm(output_path, force=True)

# Generate the documentation
Doxygen.generate_docs(DOXYFILE_PATH)
Moxygen.generate_docs(
    DOXYGEN_XML_PATH,
    Path.joinpath(MOXYGEN_MD_PATH, "%s.md"),
    separate_classes=True,
    language="cpp"
)
