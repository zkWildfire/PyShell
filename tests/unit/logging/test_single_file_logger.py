from pathlib import Path
from pyshell.logging.single_file_logger import SingleFileLogger
from typing import Any

def test_file_path_matches_ctor_arg(tmp_path: Any):
    file_path = Path.joinpath(tmp_path, "foo/bar.log")
    logger = SingleFileLogger(file_path)
    assert logger.file_path == file_path
