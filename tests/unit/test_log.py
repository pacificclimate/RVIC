import pytest
from rvic.core.log import init_logger, close_logger
import sys


def test_logger():
    logger = init_logger(log_dir="/tmp", log_level="DEBUG", verbose=False)
    with open(logger.filename, "r") as log_file:
        assert log_file.readlines()[3].split()[-1] == logger.filename

    close_logger()
    with open(logger.filename, "r") as log_file:
        assert log_file.readlines()[-1].split(">>")[0] == "INFO:close_logger"
