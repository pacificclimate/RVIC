import os
import sys
from pytest import mark
from pkg_resources import resource_filename
from rvic.convert import convert
from common import run_test
from configparser import ConfigParser


config_file = resource_filename(__name__, "../data/configs/convert.cfg")


@mark.parametrize(
    "config", [config_file],
)
def test_convert(config):
    run_test(convert, config)


@mark.parametrize(
    "config", [config_file],
)
def test_post_convert_close_logger(config):
    with open("/tmp/tmp_convert.cfg", "w") as tmp_file:
        parser = ConfigParser()
        parser.read(config)
        parser["UHS_FILES"]["STATION_FILE"] = ""
        parser.write(tmp_file)

    try:
        convert("/tmp/tmp_convert.cfg")
    except:
        assert sys.stdout == sys.__stdout__

    os.remove("/tmp/tmp_convert.cfg")
