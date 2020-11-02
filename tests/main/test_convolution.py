import os
import pytest
from pkg_resources import resource_filename
from rvic.convolution import convolution
from common import run_test, check_close_logger_call
from rvic.core.config import read_config


config_file = resource_filename(__name__, "../data/configs/convolve.cfg")
config_dict = read_config(config_file)


@pytest.mark.online
@pytest.mark.parametrize(
    "config", [config_file, config_dict],
)
def test_convolution(config):
    convolution(config)
    check_close_logger_call()


def test_invalid_input():
    invalid_config = config_dict
    invalid_config["DOMAIN"]["FILE_NAME"] = "./tests/data/samples/invalid_domain.nc"

    with pytest.raises(FileNotFoundError):
        convolution(invalid_config)
    check_close_logger_call()
