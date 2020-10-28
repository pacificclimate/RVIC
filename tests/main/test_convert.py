import os
from pytest import mark
from pkg_resources import resource_filename
from rvic.convert import convert
from common import run_test


@mark.parametrize(
    "config",
    [
        (
            resource_filename(__name__, '../data/configs/convert.cfg')
        )
    ],
)
def test_convert(config):
    run_test(convert, config)