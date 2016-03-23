import numpy as np
import pandas as pd
import sys
from fbpca import pca


def svd(matrix, k):
    ''' Provide a wrapper for the chosen SVD routine. '''
    U, s, V = pca(matrix, k=k)
    return U, s, V


def check_inertia(eigenvalues, threshold=0.8):
    ''' Check the variables that are above a certain inertia threshold. '''
    cumsum = np.cumsum(eigenvalues)
    total_inertia = cumsum[-1]
    ratios = [inertia / total_inertia for inertia in cumsum]
    check = [ratio > threshold for ratio in ratios]
    return ratios, check


def rescale(series, new_min=0, new_max=1):
    ''' Rescale a from 'new_min' to 'new_max' using the min-max method. '''
    old_min = series.min()
    old_max = series.max()
    series = series.apply(lambda x: (x - old_min) / (old_max - old_min) * (new_max - new_min) + new_min)
    return series


def progress_bar(array, bar_length, ncp):
    ''' Compute a progress bar in stdout. '''

    for i in range(len(array[0:ncp])):
        percent = array[i] / array[-1]
        hashes = '#' * round(percent * bar_length)
        spaces = ' ' * (bar_length - len(hashes))
        left_spaces = (6 - len(str('eig{}'.format(i + 1)))) * ' '
        sys.stdout.write('\r\neig{0}: [{1}] {2}%'.format(
            str(i + 1) + left_spaces, hashes + spaces, round(percent * 100)))
        sys.stdout.flush()
