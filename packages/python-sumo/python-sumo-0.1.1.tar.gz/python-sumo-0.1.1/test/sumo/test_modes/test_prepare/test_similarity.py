from sumo.modes.prepare import similarity
import numpy as np
import pytest


def _distance_testing(func, val):
    assert func in [similarity.euclidean_dist, similarity.chi_squared_dist, similarity.agreement_dist]

    assert np.allclose(func(np.array([1, 2]), np.array([1, 2])), 0)
    assert np.allclose(func(np.arange(16), np.arange(16)), 0)

    v = np.array([1 if i != 0 else 2 for i in range(100)])
    assert np.allclose(func(v, np.ones(100)), val / 100)

    assert np.allclose(func(np.array([1, 1, 1]), np.array([1, 1, 2])), val / 3)
    assert np.allclose(func(np.array([1, np.nan, 1]), np.array([1, np.nan, 2])), val / 2)
    assert np.allclose(func(np.array([np.nan, 1, 1]), np.array([1, np.nan, 2])), val)

    assert np.allclose(func(np.array([np.nan, 1, 1]), np.array([1, np.nan, 2]), missing=0.5), np.nan, equal_nan=True)
    assert np.allclose(func(np.array([np.nan, 1]), np.array([1, np.nan])), np.nan, equal_nan=True)

    with pytest.raises(AssertionError):
        func(np.array([1]), np.array([1, 1]))

    with pytest.raises(AttributeError):
        func([2], [3])


def test_euclidean_dist():
    _distance_testing(func=similarity.euclidean_dist, val=1.)


def test_chi_squared_dist():
    _distance_testing(func=similarity.chi_squared_dist, val=1. / 3)


def test_agreement_dist():
    _distance_testing(func=similarity.agreement_dist, val=1)
