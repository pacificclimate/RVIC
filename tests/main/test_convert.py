import os
import sys
import pytest
from pkg_resources import resource_filename
from rvic.convert import convert
from rvic.core.log import close_logger
from common import run_test
from configparser import ConfigParser, InterpolationMissingOptionError


config_file = resource_filename(__name__, "../data/configs/convert.cfg")


@pytest.mark.parametrize(
    "config", [config_file],
)
def test_convert(config):
    run_test(convert, config)


def test_invalid_input():
    with open("/tmp/tmp_convert.cfg", "w") as tmp_file:
        parser = ConfigParser()
        parser.read(config_file)
        parser["DOMAIN"]["FILE_NAME"] = "./tests/data/samples/invalid_domain.nc"
        parser.write(tmp_file)

    with pytest.raises(InterpolationMissingOptionError):
        convert("/tmp/tmp_convert.cfg")
    assert sys.stdout == sys.__stdout__
    assert sys.stderr == sys.__stderr__

    os.remove("/tmp/tmp_convert.cfg")
