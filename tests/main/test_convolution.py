import os
import sys
import pytest
from pytest_mock import mocker
from pkg_resources import resource_filename
from rvic.convolution import convolution
from common import run_test
from rvic.core.config import read_config


config_file = resource_filename(__name__, "../data/configs/convolve.cfg")
config_dict = read_config(config_file)


@pytest.mark.online
@pytest.mark.parametrize(
    "config", [config_file, config_dict],
)
def test_convolution(config):
    convolution(config)


def test_invalid_input(mocker):
    invalid_config = config_dict["OPTIONS"]["CALENDAR"] = ""
    mocked_close_logger = mocker.patch("rvic.core.log.close_logger")
    with pytest.raises(BaseException):
        run_test(convolution, invalid_config)
        mocked_close_logger.assert_called()
