#!/usr/bin/env python3
import argparse
from pathlib import Path
from pyshell import PyShell, PyShellOptions, AbortOnFailure, NativeBackend, \
    MultiFileLogger
from pyshell.modules import Doxygen, Shell
import sys

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

#
# Constants
#

# Path to the directory containing this script
SCRIPT_DIR = Path(__file__).parent

# Path that logs will be written to
LOGS_DIR = ".logs"

# Path to the doxygen configuration file
DOXYFILE_PATH = SCRIPT_DIR.joinpath("doxygen", "doxyfile")

# Path to the directory that Doxygen will generate documentation in
DOCS_DIR = SCRIPT_DIR.joinpath(".docs")

# Path to the directory that Doxygen will place its HTML output in
DOXYGEN_HTML_DIR = DOCS_DIR.joinpath("html")

# Path in the gh-pages branch that Doxygen files will be copied to
# Note that files should not be copied to this path when not in the gh-pages
#   branch as this is a folder used by this repository.
DOCS_HTML_DIR = SCRIPT_DIR.joinpath("doxygen")

# Initialize a PyShell instance for running commands
pyshell = PyShell(
    NativeBackend(),
    MultiFileLogger(
        LOGS_DIR,
        print_cmd_header=True,
        print_cmd_footer=True
    ),
    AbortOnFailure(),
    PyShellOptions(
        verbose=args.verbose
    ),
    cwd = SCRIPT_DIR
)

# If the --clean flag was specified, delete generated directories
if args.clean:
    Shell.rm(LOGS_DIR, force=True)
    Shell.rm(DOCS_DIR, force=True)
    Shell.rm(output_path, force=True)

# If the --publish flag was specified, start by using mkdocs to push to build
#   and push the latest mkdocs pages to the gh-pages branch.
# This is necessary to ensure that the gh-pages branch is up to date before
#   adding the doxygen documentation, which may get cleaned out by mkdocs'
#   gh-deploy command.
if args.publish:
    # Make sure all local changes are committed before allowing publishing
    if Shell.run("git", ["status", "--porcelain"]).output.strip():
        print(
            "Error: Cannot publish documentation with uncommitted changes.",
            file=sys.stderr
        )
        print(
            "Please commit or stash your changes before publishing.",
            file=sys.stderr
        )
        exit(1)

    Shell.run("mkdocs", "gh-deploy")

# Generate the documentation
# Note that this must be done in the current branch, not in the gh-pages branch.
Doxygen.generate_docs(DOXYFILE_PATH)

# If the --publish flag was specified, copy the doxygen documentation to the
#   gh-pages branch and push it.
if args.publish:
    # Get the branch that's currently checked out
    curr_branch = Shell.run("git", ["branch", "--show-current"]).output.strip()

    # Switch to the gh-pages branch, which will remove the repo files and leave
    #   only the files that are hosted by GitHub Pages.
    Shell.run("git", ["switch", "gh-pages"])

    # Pull the commit that was just created by the mkdocs gh-deploy command
    Shell.run("git", "pull")

    # Copy the doxygen documentation to the target directory
    Shell.cp(DOXYGEN_HTML_DIR, DOCS_HTML_DIR)

    # Push the doxygen files to the gh-pages branch
    Shell.run("git", ["add", DOCS_HTML_DIR])
    Shell.run("git", ["commit", "-m", "[PyShell] Add doxygen documentation"])
    Shell.run("git", "push")

    # Switch back to the original branch as cleanup
    Shell.run("git", ["switch", curr_branch])
