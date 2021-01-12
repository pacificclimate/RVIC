import os
import pytest
from pathlib import Path
from rvic.parameters import parameters
from common import run_test, check_close_logger_call
from rvic.core.config import read_config


config_file = str(Path(__file__).parents[1]) + "/data/configs/parameters.cfg"
config_dict = read_config(config_file)


@pytest.mark.parametrize(
    ("config", "numofproc"), [(config_file, 2), (config_dict, 2)],
)
def test_parameters(config, numofproc):
    run_test(parameters, config, numofproc)
    check_close_logger_call()


def test_invalid_input():
    invalid_config = config_dict
    invalid_config["DOMAIN"]["FILE_NAME"] = "./tests/data/samples/invalid_domain.nc"

    with pytest.raises(FileNotFoundError):
        parameters(invalid_config)
    check_close_logger_call()
