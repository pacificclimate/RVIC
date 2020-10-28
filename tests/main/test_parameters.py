import os
from pytest import mark
from pkg_resources import resource_filename
from rvic.parameters import parameters
from common import run_test

@mark.parametrize(
    "config",
    [
        (
            resource_filename(__name__, '../data/configs/parameters.cfg')
        )
    ],
)
def test_parameters(config):
    run_test(parameters, config)