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


def interpolation_bilinear(x, y, x1, x2, y1, y2, z11, z21, z22, z12):
    '''
    The points (x_i, y_i) and values z_ij are connected as follows:
    Starting from lower left going in mathematically positive direction, i.e. counter clockwise.
    Therefore: (x1,y1,z11), (x2,y1,z21), (x2,y2,z22), (x1,y2,z12).
    '''
    t = (x - x1) / (x2 - x1)
    s = (y - y1) / (y2 - y1)
    v1 = (1.0 - t) * (1.0 - s) * z11
    v2 = t * (1.0 - s) * z21
    v3 = t * s * z22
    v4 = (1.0 - t) * s * z12
    ret = v1 + v2 + v3 + v4
    return ret
