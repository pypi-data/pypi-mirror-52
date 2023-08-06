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


def interpolation_linear(x, x1, x2, y1, y2):
    """
    Linear interpolation
    returns (y2 - y1) / (x2 - x1) * (x - x1) + y1
    """
    m = (y2 - y1) / (x2 - x1)
    t = (x - x1)
    return m * t + y1
