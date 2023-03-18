import os
from pathlib import Path
from pyshell import PyShell
from pyshell.modules.git import Git
from typing import Any

def get_dir_size(start_path: str | Path) -> int:
    """
    Calculates the size of a directory's contents in bytes.
    @param start_path: The path to the directory to calculate the size of.
    @return: The size of the directory's contents in bytes.
    """
    start_path = Path(start_path)
    total_size = 0

    for dirpath, _, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # Ignore symbolic links
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def test_clone_pyshell_repository(tmp_path: Any):
    # Set up a shell in the temporary directory
    pyshell = PyShell()
    pyshell.cd(tmp_path)

    # Run the command
    result = Git.clone("https://github.com/MYTX-Wildfire/PyShell.git")
    assert result.success


def test_clone_pyshell_with_custom_path(tmp_path: Any):
    # Set up a shell in the temporary directory
    pyshell = PyShell()
    pyshell.cd(tmp_path)

    # Run the command
    dir_name = "foo"
    result = Git.clone("https://github.com/MYTX-Wildfire/PyShell.git", dir_name)
    assert result.success
    assert Path(tmp_path, dir_name).exists()

def test_shallow_clone_pyshell_repository(tmp_path: Any):
    # Set up a shell in the temporary directory
    pyshell = PyShell()
    pyshell.cd(tmp_path)

    # Run the command
    result = Git.clone(
        "https://github.com/MYTX-Wildfire/PyShell.git",
        output_directory="full"
    )
    assert result.success
    result = Git.clone(
        "https://github.com/MYTX-Wildfire/PyShell.git",
        output_directory="shallow",
        depth=1
    )

    # Make sure the shallow clone is smaller than the full clone
    full_size = get_dir_size(Path(tmp_path, "full"))
    shallow_size = get_dir_size(Path(tmp_path, "shallow"))
    assert shallow_size < full_size
