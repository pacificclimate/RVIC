import os
import sys
import pytest
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


def test_invalid_input():
    invalid_config = config_dict
    invalid_config["DOMAIN"]["FILE_NAME"] = "./tests/data/samples/invalid_domain.nc"

    with pytest.raises(FileNotFoundError):
        convolution(invalid_config)
    assert sys.stdout == sys.__stdout__
    assert sys.stderr == sys.__stderr__
