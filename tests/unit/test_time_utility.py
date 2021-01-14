# -------------------------------------------------------------------- #
# Unit tests for make_uh.py
from rvic.core.time_utility import ord_to_datetime, Dtime
from rvic.core.share import TIMEUNITS
from netCDF4 import date2num
import cftime


def test_ord_to_datetime():
    # Independence day
    date = cftime.DatetimeGregorian(1776, 7, 4, 12, 0, 0, 0)
    print(date)
    ord_time = date2num(date, TIMEUNITS)
    print(ord_time)
    # Independence day (note that this fails if date has microseconds != 0)
    print(ord_to_datetime(ord_time, TIMEUNITS))
    assert ord_to_datetime(ord_time, TIMEUNITS) == date


def test_dtime():
    dt = Dtime(
        "2014-12-01-00", "ndays", 5, None, "ndays", 5, None, "noleap", 3600.00001
    )
    assert dt.timestamp.year == 2014
    assert dt.timestamp.month == 12
    assert dt.timestamp.day == 1
    assert dt.timestamp.hour == 0
    dt.advance_timestep()
    assert dt.timestamp.year == 2014
    assert dt.timestamp.month == 12
    assert dt.timestamp.day == 1
    assert dt.timestamp.hour == 1
