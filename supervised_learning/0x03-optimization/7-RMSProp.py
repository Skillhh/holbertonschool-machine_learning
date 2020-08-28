#!/usr/bin/env python3
""" RMSProp optimization """
import numpy as np


def update_variables_RMSProp(alpha, beta2, epsilon, var, grad, s):
    """ update_variables_RMSProp

    Args:
        alpha is the learning rate
        beta2 is the RMSProp weight
        epsilon is a small number to avoid division by zero
        var is a numpy.ndarray containing the variable to be updated
        grad is a numpy.ndarray containing the gradient of var
        s is the previous second moment of var

    Returns:
        the updated variable and the new moment, respectively
    """
    s = beta2 * s + (1 - beta2) * (grad * grad)
    var -= alpha * grad / (np.sqrt(s) + epsilon)

    return var, s
