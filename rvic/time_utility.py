"""
time_utility.py
"""

from netCDF4 import num2date, date2num
from datetime import datetime
from dateutil.relativedelta import relativedelta
from share import TIMEUNITS, SECSPERDAY, MINSPERDAY, HOURSPERDAY, TIMESTAMPFORM
from logging import getLogger
from log import LOG_NAME

# -------------------------------------------------------------------- #
# create logger
log = getLogger(LOG_NAME)
# -------------------------------------------------------------------- #


# -------------------------------------------------------------------- #
# RVIC Time Class
class Dtime(object):
    """ A Time Module for handling flags and timesteps """

    # ---------------------------------------------------------------- #
    # Setup Dtim object
    def __init__(self, start_date, stop_option, stop_n, stop_date,
                 rest_option, rest_n, rest_date, calendar, dt):

        self.start_date = datetime.strptime(start_date, TIMESTAMPFORM)
        self.calendar = calendar
        self.dt = float(dt) / float(SECSPERDAY)  # In days

        # Setup Current Time
        self.timestamp = self.start_date
        self.time_ord = date2num(self.timestamp, TIMEUNITS, calendar=self.calendar)

        # Stop option
        self.stop_option = stop_option
        self.stop_n = stop_n
        if self.stop_option == 'date':
            date = map(int, stop_date.split('-'))
            self.stop_date = datetime(*date)
        else:
            self.stop_date = False

        # Rest option
        self.rest_option = rest_option
        self.rest_n = rest_n
        if self.rest_option == 'date':
            date = map(int, rest_date.split('-'))
            self.rest_date = datetime(*date)
        else:
            self.rest_date = False

        # Counters
        self.timesteps = 0
        self.statefiles = 0

        # Flags
        self.stop_flag = False
        self.rest_flag = False

    def advance_timestep(self):
        self.time_ord += self.dt
        self.timestamp = ord_to_datetime(self.time_ord, TIMEUNITS, calendar=self.calendar)
        self.timesteps += 1
        self.stop_flag = self.stop()
        self.rest_flag = self.rest()
        return self.timestamp
    # ---------------------------------------------------------------- #

    # ---------------------------------------------------------------- #
    # Time to stop run
    def stop(self):
        flag = False
        if self.stop_option == 'nsteps':
            if self.timesteps >= self.stop_n:
                flag = True
        elif self.stop_option == 'nseconds':
            if (self.timesteps * self.dt / SECSPERDAY) >= self.stop_n:
                flag = True
        elif self.stop_option == 'nminutes':
            if (self.timesteps * self.dt / MINSPERDAY) >= self.stop_n:
                flag = True
        elif self.stop_option == 'nhours':
            if (self.timesteps * self.dt / HOURSPERDAY) >= self.stop_n:
                flag = True
        elif self.stop_option == 'ndays':
            if (self.timesteps * self.dt) >= self.stop_n:
                flag = True
        elif self.stop_option == 'nmonths':
            if relativedelta(self.timestamp, self.start_date).months >= self.stop_n:
                flag = True
        elif self.stop_option == 'nyears':
            if relativedelta(self.timestamp, self.start_date).years >= self.stop_n:
                flag = True
        elif self.stop_option == 'date':
            if self.timestamp >= self.stop_date:
                flag = True
        elif self.stop_option == 'end':
            if self.timestamp >= self.end:
                flag = True
        else:
            raise ValueError('unknown stop_option %s' %self.stop_option)
        return flag
    # ---------------------------------------------------------------- #

    # ---------------------------------------------------------------- #
    # Time to write restart?
    def rest(self):
        flag = False
        if self.rest_option == 'nsteps':
            if self.timesteps >= self.rest_n:
                flag = True
        elif self.rest_option == 'nseconds':
            if (self.timesteps * self.dt / SECSPERDAY) >= self.rest_n:
                flag = True
        elif self.rest_option == 'nminutes':
            if (self.timesteps * self.dt / MINSPERDAY) >= self.rest_n:
                flag = True
        elif self.rest_option == 'nhours':
            if (self.timesteps * self.dt / HOURSPERDAY) >= self.rest_n:
                flag = True
        elif self.rest_option == 'ndays':
            if (self.timesteps * self.dt) >= self.rest_n:
                flag = True
        elif self.rest_option == 'nmonths':
            if relativedelta(self.timestamp, self.start_date).months >= self.rest_n:
                flag = True
        elif self.rest_option == 'nyears':
            if relativedelta(self.timestamp, self.start_date).years >= self.rest_n:
                flag = True
        elif self.rest_option == 'date':
            if self.timestamp >= self.rest_date:
                flag = True
        elif self.rest_option == 'end':
            if self.timestamp >= self.end:
                flag = True
        else:
            raise ValueError('unknown rest_option %s' %self.rest_option)
        return flag
    # ---------------------------------------------------------------- #
# -------------------------------------------------------------------- #

# -------------------------------------------------------------------- #
def ord_to_datetime(time, units, calendar='standard'):
    """
    netCDF4.num2date yields a fake datetime object, this function converts
    converts that back to a real datetime object
    """
    # this is the netCDF4.datetime object
    # if the calendar is standard, t is already a real datetime object
    t = num2date(time, units, calendar=calendar)
    if calendar in ['proleptic_gregorian', 'standard', 'gregorian']:
        return t
    else:
        return datetime(t.year, t.month, t.day, t.hour, t.minute, t.second)
# -------------------------------------------------------------------- #