import os
from pathlib import Path
from pyshell.logging.multi_file_logger import MultiFileLogger
import pytest
from typing import Any

def test_log_path_matches_ctor_arg(tmp_path: Any):
    log_path = Path.joinpath(tmp_path, "foo/bar")
    logger = MultiFileLogger(log_path)
    assert logger.output_dir == log_path


def test_logger_creates_output_dir(tmp_path: Any):
    log_path = Path.joinpath(tmp_path, "foo/bar")
    MultiFileLogger(log_path)
    assert os.path.isdir(log_path)


def test_logger_clears_output_dir(tmp_path: Any):
    log_path = Path.joinpath(tmp_path, "foo/bar")
    os.makedirs(log_path)
    with open(Path.joinpath(log_path, "foo.txt"), "w") as f:
        f.write("foo")
    MultiFileLogger(log_path)
    assert not os.listdir(log_path)


def test_skip_clean_output_dir(tmp_path: Any):
    log_path = Path.joinpath(tmp_path, "foo/bar")
    os.makedirs(log_path)
    with open(Path.joinpath(log_path, "foo.txt"), "w") as f:
        f.write("foo")
    MultiFileLogger(log_path, clean_logs_dir=False)
    assert os.listdir(log_path)


def test_logger_throws_if_output_dir_is_file(tmp_path: Any):
    log_path = Path.joinpath(tmp_path, "foo/bar")
    log_path.parent.mkdir(parents=True)
    with open(log_path, "w") as f:
        f.write("foo")
    with pytest.raises(ValueError):
        MultiFileLogger(log_path)
