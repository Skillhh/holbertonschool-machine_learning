#!/usr/bin/env python3
""" import """
import numpy as np


def one_hot_encode(Y, classes):
    """ one_hot_encode - converts a numeric label vector
                         into a one-hot matrix.

    Args:
        Y       containing numeric class labels.
        classes is the maximum number of classes.

    Return:
        Returns: a one-hot encoding of Y with shape.
    """
    if len(Y) == 0 or type(Y) is not np.ndarray:
        return None
    elif type(classes) is not int or classes < np.amax(Y):
        return None

    one_hot = np.zeros((classes, Y.shape[0]))
    one_hot[Y, np.arange(Y.shape[0])] = 1

    return one_hot
