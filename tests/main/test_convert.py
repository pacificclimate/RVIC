import os
import sys
import pytest
from pytest_mock import mocker
from pkg_resources import resource_filename
from rvic.convert import convert
from rvic.core.log import close_logger
from common import run_test
from configparser import ConfigParser


config_file = resource_filename(__name__, "../data/configs/convert.cfg")


def test_convert(mocker):
    mocked_close_logger = mocker.patch("rvic.core.log.close_logger")
    run_test(convert, config_file)
    mocked_close_logger.assert_called()


def test_invalid_input(mocker):
    with open("/tmp/tmp_convert.cfg", "w") as tmp_file:
        parser = ConfigParser()
        parser.read(config_file)
        parser["UHS_FILES"]["STATION_FILE"] = ""
        parser.write(tmp_file)

    mocked_close_logger = mocker.patch("rvic.core.log.close_logger")
    with pytest.raises(BaseException):
        run_test(convert, "/tmp/tmp_convert.cfg")
    mocked_close_logger.assert_called()

    os.remove("/tmp/tmp_convert.cfg")
