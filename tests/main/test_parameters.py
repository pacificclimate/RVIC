import os
import sys
from pytest import mark
from pkg_resources import resource_filename
from rvic.parameters import parameters
from common import run_test
from rvic.core.config import read_config


config_file = resource_filename(__name__, "../data/configs/parameters.cfg")
config_dict = read_config(config_file)


@mark.parametrize(
    ("config", "numofproc"), [(config_file, 2), (config_dict, 2)],
)
def test_parameters(config, numofproc):
    run_test(parameters, config, numofproc)


invalid_config = config_dict["OPTIONS"]["CASEID"] = ""


@mark.parametrize(
    "config", [invalid_config],
)
def test_post_parameters_close_logger(config):
    try:
        parameters(config)
    except:
        assert sys.stdout == sys.__stdout__
