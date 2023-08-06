"""Utility functions for Machine Learning"""

import numpy as np


def make_multiclass(N=500, D=2, K=3):
    """
    Generate spiral-shaped data
    N: number of points per class
    D: dimensionality
    K: number of classes
    """

    np.random.seed(0)
    X = np.zeros((N * K, D))
    y = np.zeros(N * K)
    for j in range(K):
        ix = range(N * j, N * (j + 1))
        # radius
        r = np.linspace(0.0, 1, N)
        # theta
        t = np.linspace(j * 4, (j + 1) * 4, N) + np.random.randn(N) * 0.2
        X[ix] = np.c_[r * np.sin(t), r * np.cos(t)]
        y[ix] = j
    return X, y


def vectorize_sequences(sequences, dimension=10000):
    """One-hot encode a vector of sequences into a binary matrix (number of sequences, dimension)"""

    # Example : [[3, 5]] -> [[0. 0. 0. 1. 0. 1. 0...]]

    results = np.zeros((len(sequences), dimension))
    # set specific indices of results[i] to 1s
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results
