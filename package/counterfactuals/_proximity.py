"""
Provides a single function for calculating a proximetry matrix for a rf.
"""

import os
import ctypes
import numpy as np
from numpy.ctypeslib import ndpointer



_proximitylib = ctypes.cdll.LoadLibrary(
    os.path.join(os.path.dirname(__file__), "_prox.so"))
_proximity = _proximitylib.get_indexes
_proximity.restype = None
_proximity.argtypes = [
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
    ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
    ndpointer(ctypes.c_bool, flags="C_CONTIGUOUS"),
    ndpointer(ctypes.c_bool, flags="C_CONTIGUOUS"),
    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS")]



def proximity(
    n_trees,
    n_other,
    n_treated,
    leaves_other,
    leaves_treated,
    not_in_other,
    not_in_treated):

    # buffers to write the matching indexes and distances into.
    proximity = np.zeros((n_other, n_treated), np.float64)

    _proximity(
        n_trees,
        n_other,
        n_treated,
        leaves_other,
        leaves_treated,
        not_in_other,
        not_in_treated,
        proximity)

    return proximity;
