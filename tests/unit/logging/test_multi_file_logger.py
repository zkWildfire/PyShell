from pathlib import Path
from pyshell.logging.multi_file_logger import MultiFileLogger
from typing import Any

def test_log_path_matches_ctor_arg(tmp_path: Any):
    log_path = Path.joinpath(tmp_path, "foo/bar")
    logger = MultiFileLogger(log_path)
    assert logger.output_dir == log_path
