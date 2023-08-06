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


from math import exp
from mathtoolspy.utils.mathconst import ONE_OVER_SQRT_OF_TWO_PI


def density_normal_dist(x):
    """ Density function for normal distribution
    @param x: float value
    @return value of normal density function
    """
    return ONE_OVER_SQRT_OF_TWO_PI * exp(-0.5 * x * x)


def normal_density(x):
    density_normal_dist(x)


def cdf_abramowitz_stegun(x):
    """
    The cumulative distribution function of the standard normal distribution.
    The standard implementation, following Abramowitz/Stegun, (26.2.17).
    """
    if x >= 0:
        # if x > 7.0:
        #    return 1 - ONE_OVER_SQRT_OF_TWO_PI * exp(-0.5*x*x)/sqrt(1.0+x*x)
        result = 1.0 / (1.0 + 0.2316419 * x)
        ret = 1.0 - ONE_OVER_SQRT_OF_TWO_PI * exp(-0.5 * x * x) * (
            result * (0.31938153 +
                      result * (-0.356563782 +
                                result * (1.781477937 +
                                          result * (-1.821255978 +
                                                    result * 1.330274429)))))
        return ret

    if x <= 0:
        # if x < -7.0:
        #    return 1 - one_over_sqrt_of_two_pi() * exp(-0.5*x*x)/sqrt(1.0+x*x)
        result = 1.0 / (1.0 - 0.2316419 * x)
        ret = ONE_OVER_SQRT_OF_TWO_PI * exp(-0.5 * x * x) * (
            result * (0.31938153 +
                      result * (-0.356563782 +
                                result * (1.781477937 +
                                          result * (-1.821255978 +
                                                    result * 1.330274429)))))

        return ret


def normal_cdf(x):
    return cdf_abramowitz_stegun(x)
