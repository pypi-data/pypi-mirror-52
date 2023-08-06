# -*- coding: utf-8 -*-

# mathtoolspy
# -----------
# A fast, efficient Python library for mathematically operations, like
# integration, solver, distributions and other useful functions.
# 
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.3, copyright Wednesday, 18 September 2019
# Website:  https://github.com/sonntagsgesicht/mathtoolspy
# License:  Apache License 2.0 (see LICENSE file)


"""
The MathFct contains some mathematically method, which are not supported by the Python lib.
"""
import operator
from .mathconst import DOUBLE_TOL
from functools import reduce


def abs_sign(a, b):
    ''' The absolute value of A with the sign of B.'''
    return abs(a) if b >= 0 else -abs(a)


def sign(x):
    '''
    Returns the sign of the double number x.
    -1 if x < 0; 1 if x > 0 and 0 if x == 0
    '''
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


def float_equal(x, y, tol=DOUBLE_TOL):
    return abs(x - y) < tol


def prod(factors):
    """
    The product of the given factors (iterable)
    :param factors:
    :return:
    """
    return reduce(operator.mul, factors, 1.0)


def get_grid(start, end, nsteps=100):
    """
    Generates a equal distanced list of float values with nsteps+1 values, begining start and ending with end.

    :param start: the start value of the generated list.

    :type float

    :param end: the end value of the generated list.

    :type float

    :param nsteps: optional the number of steps (default=100), i.e. the generated list contains nstep+1 values.

    :type int


    """
    step = (end-start) / float(nsteps)
    return [start + i * step for i in range(nsteps+1)]


class FctWithCount(object):
    def __init__(self, fct):
        self.fct = fct
        self.number_of_calls = 0

    def __call__(self, x):
        self.number_of_calls += 1
        return self.fct(x)


class CompositionFct:
    def __init__(self, *fcts):
        self.fcts = fcts[::-1]

    def __call__(self, x):
        ret = x
        for fct in self.fcts:
            ret = fct(ret)
        return ret
