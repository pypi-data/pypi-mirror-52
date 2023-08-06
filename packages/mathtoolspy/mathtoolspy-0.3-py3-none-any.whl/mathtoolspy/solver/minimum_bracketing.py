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


from mathtoolspy.utils.mathconst import DOUBLE_TOL, GOLD
from mathtoolspy.utils.math_fcts import abs_sign
from mathtoolspy.solver.minimize_algorithm_1dim_brent import shift

''' Maximum magnification allowed for a parabolic-fit step.'''
GLIMIT = 100.0
''' Used to prevent any possible division by zero. '''
TINY = 1.0e-20


def mn_brak(a, b, fct):
    ax = a
    bx = b
    ulim = u = r = q = fu = 0.0
    fa = fct(a)
    fb = fct(b)
    if fb > fa:
        ax, bx = (bx, ax)
        fa, fb = (fb, fa)
    cx = bx + GOLD * (bx - ax)
    fc = fct(cx)
    while fb > fc:
        r = (bx - ax) * (fb - fc)
        q = (bx - cx) * (fb - fa)
        u = bx - ((bx - cx) * q - (bx - ax) * r) / (2.0 * abs_sign(max(abs(q - r), TINY), q - r))
        ulim = bx + GLIMIT * (cx - bx)
        if (bx - u) * (u - cx) > 0.0:
            fu = fct(u)
            if fu < fc:
                ax, bx, fa, fb = (bx, u, fb, fu)
                return (ax, bx, cx, fa, fb, fc)
            elif fu > fb:
                cx, fc = (u, fu)
                return (ax, bx, cx, fa, fb, fc)
            u = cx + GOLD * (cx - bx)
            fu = fct(u)
        elif (cx - u) * (u - ulim) > 0.0:
            fu = fct(u)
            if fu < fc:
                bx, cx = (cx, u)
                u = cx + GOLD * (cx - bx)
                fb, fc = (fc, fu)
                fu = fct(u)
        elif (u - ulim) * (ulim - cx) >= 0.0:
            u = ulim
            fu = fct(u)
        else:
            u = cx + GOLD * (cx - bx)
            fu = fct(u)
        ax, bx, cx, fa, fb, fc = (bx, cx, u, fb, fc, fu)
    return (ax, bx, cx, fa, fb, fc)


def mn_brak_(a, b, fct):
    ax = a
    bx = b
    ulim = u = r = q = fu = dum = 0.0
    fa = fct(a)
    fb = fct(b)
    if fb > fa:
        dum, ax, bx = shift(ax, bx, dum)
        dum, fb, fa = shift(fb, fa, dum)

    cx = bx + GOLD * (bx - ax)
    fc = fct(cx)
    while fb > fc:
        r = (bx - ax) * (fb - fc)
        q = (bx - cx) * (fb - fa)
        u = bx - ((bx - cx) * q - (bx - ax) * r) / (2.0 * abs_sign(max(abs(q - r), TINY), q - r))
        ulim = bx + GLIMIT * (cx - bx)

        if (bx - u) * (u - cx) > 0.0:
            fu = fct(u)
            if fu < fc:
                ax = bx
                bx = u
                fa = fb
                fb = fu
                return (ax, bx, cx, fa, fb, fc)
            elif fu > fb:
                cx = u
                fc = fu
                return (ax, bx, cx, fa, fb, fc)
            u = cx + GOLD * (cx - bx)
            fu = fct(u)
        elif (cx - u) * (u - ulim) > 0.0:
            fu = fct(u)
            if fu < fc:
                bx, cx, u = shift(cx, u, cx + GOLD * (cx - bx))
                fb, fc, fu = shift(fc, fu, fct(u))
        elif (u - ulim) * (ulim - cx) >= 0.0:
            u = ulim
            fu = fct(u)
        else:
            u = cx + GOLD * (cx - bx)
            fu = fct(u)
        ax, bx, cx = shift(bx, cx, u)
        fa, fb, fc = shift(fb, fc, fu)

    return (ax, bx, cx, fa, fb, fc)


def minimum_bracketing(fct, initial_value=0.0, natural_length=1.0 + DOUBLE_TOL):
    '''
    Given a function func, and given distinct inital points ax and bx, this routine searches
    in the downhill direction (defined by the function as evaluated at the initial points)
    and returns new points at ax, bx, cx that bracket a minimum of the function.
    Also returned are the function values at the three points.
    See Press, et al. (1992) "Numerical recipes in C", 2nd ed., p.400.
    '''

    def _minimum_bracketing(a, b, fct):
        v = mn_brak(a, b, fct)
        fa = v[3]
        fb = v[4]
        fc = v[5]
        if not (fa > fb and fb < fc):
            return False
        # Return the three bracketing points.
        return (v[0], v[1], v[2])

    ta = initial_value if initial_value != None else 0.0
    tb = ta + natural_length
    ret = _minimum_bracketing(ta, tb, fct)
    return ret


def simple_bracketing(func, a, b, precision=TINY):
    """ find root by simple_bracketing an interval

    :param callable func: function to find root
    :param float a: lower interval boundary
    :param float b: upper interval boundary
    :param float precision: max accepted error
    :rtype: tuple
    :return: :code:`(a, m, b)` of last recursion step with :code:`m = a + (b-a) *.5`

    """
    fa, fb = func(a), func(b)
    if fb < fa:
        f = (lambda x: -func(x))
        fa, fb = fb, fa
    else:
        f = func

    if not fa <= 0. <= fb:
        msg = "simple_bracketing function must be loc monotone between %0.4f and %0.4f \n" % (a, b)
        msg += "and simple_bracketing 0. between  %0.4f and %0.4f." % (fa, fb)
        raise RuntimeError(msg)

    m = a + (b-a) * 0.5
    if abs(b - a) < DOUBLE_TOL and abs(fb - fa) < precision:
        return a, m, b

    a, b = (m, b) if f(m) < 0 else (a, m)
    return simple_bracketing(f, a, b, precision)
