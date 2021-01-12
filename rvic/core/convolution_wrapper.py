# -*- coding: utf-8 -*-
"""
convolution_wrapper.py

ctypes wrapper for rvic_convolution.c

gcc -shared -o rvic_convolution.so rvic_convolution.c
"""

import os
import distutils.sysconfig
import sys
import numpy as np
import ctypes

ext_suffix_var = "SO"
if sys.version_info[:2] >= (3, 5):
    ext_suffix_var = "EXT_SUFFIX"

SHAREDOBJECT = "rvic_convolution" + distutils.sysconfig.get_config_var(ext_suffix_var)
LIBPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

try:
    _convolution = np.ctypeslib.load_library(SHAREDOBJECT, LIBPATH)
except ImportError as ie:
    print("error looking for shared object {0} in {1}".format(SHAREDOBJECT, LIBPATH))
    raise ImportError(ie)
except OSError as oe:
    print("error looking for shared object {0} in {1}".format(SHAREDOBJECT, LIBPATH))
    raise ImportError(oe)

_args = [
    ctypes.c_int,  # nsources
    ctypes.c_int,  # noutlets
    ctypes.c_int,  # subset_length
    ctypes.c_int,  # xsize
    np.ctypeslib.ndpointer(np.int32),  # source2outlet_ind
    np.ctypeslib.ndpointer(np.int32),  # source_y_ind
    np.ctypeslib.ndpointer(np.int32),  # source_x_ind
    np.ctypeslib.ndpointer(np.int32),  # source_time_offset
    np.ctypeslib.ndpointer(np.float64),  # unit_hydrograph
    np.ctypeslib.ndpointer(np.float64),  # aggrunin
    np.ctypeslib.ndpointer(np.float64),  # ring
]
_convolution.convolve.argtypes = _args
_convolution.convolve.restype = None

rvic_convolve = _convolution.convolve
