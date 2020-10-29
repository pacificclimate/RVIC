import pytest
import os
import numpy as np
from rvic.core.variables import Rvar
from rvic.core.history import Tape
from pathlib import Path


@pytest.mark.local
@pytest.fixture()
def rvar(scope="function"):
    dirname = Path(__file__).parent.parent
    infile = os.path.join(
        dirname, "data/samples", "sample.rvic.prm.COLUMBIA.20180516.nc"
    )
    rv = Rvar(infile, "test_case", "noleap", dirname, "NETCDF4")
    return rv


@pytest.mark.local
def test_create_tape_instance(rvar):
    history_tape = Tape(
        1.25, "test", rvar, grid_area=np.zeros((10, 11)), outtype="array"
    )
