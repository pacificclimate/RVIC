import os
import pytest
from pathlib import Path
from rvic.convert import convert
from rvic.core.log import close_logger
from common import run_test, check_close_logger_call
from configparser import ConfigParser, InterpolationMissingOptionError


config_file = str(Path(__file__).parents[1]) + "/data/configs/convert.cfg"


@pytest.mark.parametrize(
    "config", [config_file],
)
def test_convert(config):
    run_test(convert, config)
    check_close_logger_call()


def test_invalid_input():
    with open("/tmp/tmp_convert.cfg", "w") as tmp_file:
        parser = ConfigParser()
        parser.optionxform = str
        parser.read(config_file)
        parser["DOMAIN"]["FILE_NAME"] = "./tests/data/samples/invalid_domain.nc"
        parser.write(tmp_file)

    with pytest.raises(FileNotFoundError):
        convert("/tmp/tmp_convert.cfg")
    check_close_logger_call()

    os.remove("/tmp/tmp_convert.cfg")
