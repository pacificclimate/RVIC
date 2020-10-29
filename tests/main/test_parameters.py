import os
from pytest import mark
from pkg_resources import resource_filename
from rvic.parameters import parameters
from common import run_test


@mark.parametrize(
    ("config", "numofproc"),
    [(resource_filename(__name__, "../data/configs/parameters.cfg"), 2)],
)
def test_parameters(config, numofproc):
    run_test(parameters, config, numofproc)
