import os
import sys
import pytest
from pytest_mock import mocker
from pkg_resources import resource_filename
from rvic.parameters import parameters
from common import run_test
from rvic.core.config import read_config


config_file = resource_filename(__name__, "../data/configs/parameters.cfg")
config_dict = read_config(config_file)


@pytest.mark.parametrize(
    ("config", "numofproc"), [(config_file, 2), (config_dict, 2)],
)
def test_parameters(config, numofproc):
    run_test(parameters, config, numofproc)


def test_invalid_input(mocker):
    invalid_config = config_dict["OPTIONS"]["CASEID"] = ""
    mocked_close_logger = mocker.patch("rvic.core.log.close_logger")
    with pytest.raises(BaseException):
        run_test(parameters, invalid_config)
        mocked_close_logger.assert_called()
