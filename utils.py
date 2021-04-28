import numpy as np


def parametric_line(x, y):
    """
    :param x: 1D numpy array
    :param y: 1D numpy array
    :return:
    """
    if len(x) != len(y):
        raise ValueError('Arrays must be of same length')

    X = np.ones((len(x), len(y))) * np.nan
    Y = X.copy()

    for i in range(len(x)):
        X[i, :(i + 1)] = x[:(i + 1)]
        Y[i, :(i + 1)] = y[:(i + 1)]
    return X, y


def demeshgrid(arr):
    """
    Turn an ndarray created by meshgrid back to 1D array
    :param arr: array of dimension > 1
        This array should have been created by a meshgrid.
    :return: 1D array
    """

    dim = len(arr.shape)
    for i in range(dim):
        slice_1 = [0] * dim
        slice_2 = [1] * dim
        slice_1[i] = slice(None)
        slice_2[i] = slice(None)

        if (arr[tuple(slice_1)] == arr[tuple(slice_2)]).all():
            return arr[tuple(slice_1)]
