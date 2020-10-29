import os
import sys
from pytest import mark
from pkg_resources import resource_filename
from rvic.convolution import convolution
from common import run_test
from rvic.core.config import read_config


config_file = resource_filename(__name__, "../data/configs/convolve.cfg")
config_dict = read_config(config_file)


@mark.local
@mark.parametrize(
    "config", [config_file, config_dict],
)
def test_convolution(config):
    run_test(convolution, config)


invalid_config = config_dict["OPTIONS"]["CALENDAR"] = ""


@mark.parametrize(
    "config", [invalid_config],
)
def test_post_convolution_close_logger(config):
    try:
        convolution(config)
    except:
        assert sys.stdout == sys.__stdout__
