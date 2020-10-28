import os
from pytest import mark
from pkg_resources import resource_filename
from rvic.convolution import convolution
from common import run_test


@mark.local
@mark.parametrize(
    "config", [(resource_filename(__name__, "../data/configs/convolve.cfg"))],
)
def test_convolution(config):
    run_test(convolution, config)
