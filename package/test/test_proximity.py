import numpy as np
from math import isclose
from counterfactuals.proximity import proximity

N_TREATED = 100
N_OTHER = 1000
N_TREES = 100
TOL = 1e-6

def _do_test(
    i_treated,
    i_other,
    l_treated,
    l_other,
    test,
    n_trees=N_TREES,
    n_treated=N_TREATED,
    n_other=N_OTHER):

    not_in_treated = i_treated((n_treated, n_trees), dtype=np.bool)
    not_in_other = i_other((n_other, n_trees), dtype=np.bool)

    leaves_treated = l_treated((n_treated, n_trees), dtype=np.int32)
    leaves_other = l_other((n_other, n_trees), dtype=np.int32)

    res = proximity(
        n_treated,
        n_other,
        n_trees,
        leaves_treated,
        leaves_other,
        not_in_treated,
        not_in_other)

    assert test(res)



def test_all_0():
    """All observations in no tree and all in the same node of every tree."""
    _do_test(
        np.ones, np.ones, np.ones, np.ones,
        lambda x: isclose(sum(sum(x)), N_TREATED*N_OTHER))

def test_all_1():
    """All observations in no tree and all in the same node of every tree."""
    _do_test(
        np.ones, np.ones, np.ones, np.ones,
        lambda x: np.all(np.abs(x-1.) < TOL))

def test_all_0_1():
    """All observations in no tree and no treated in the same node as an 'other'
    in any tree."""
    _do_test(
        np.ones, np.ones, np.zeros, np.ones,
        lambda x: np.all(x < TOL))

def test_all_0_2():
    """All observations in no tree and no treated in the same node as an 'other'
    in any tree."""
    _do_test(
        np.ones, np.ones, np.ones, np.zeros,
        lambda x: np.all(x < TOL))

def test_all_0_3():
    """No treated in a tree, all 'other' in a tree and all in the same node of
    every tree."""
    _do_test(
        np.ones, np.zeros, np.ones, np.ones,
        lambda x: np.all(x < TOL))

def test_all_0_4():
    """All treated in all trees, no 'other' in any tree and all in the same nod
    of every tree."""
    _do_test(
        np.zeros, np.ones, np.ones, np.ones,
        lambda x: np.all(x < TOL))

def test_all_0_5():
    """No trees."""
    _do_test(
        np.ones, np.ones, np.ones, np.ones,
        lambda x: np.all(x < TOL),
        n_trees=0)

def test_all_0_7():
    """No treated."""
    _do_test(
        np.zeros, np.ones, np.ones, np.ones,
        lambda x: np.all(x < TOL),
        n_treated=0)

def test_all_0_8():
    """No other."""
    _do_test(
        np.zeros, np.ones, np.ones, np.ones,
        lambda x: np.all(x < TOL),
        n_other=0)
