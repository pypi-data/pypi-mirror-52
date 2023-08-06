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


class base_interpolation(object):
    """
    Basic class to interpolate given data.
    """

    def __init__(self, x_list=list(), y_list=list()):
        self.x_list = list()
        self.y_list = list()
        self.update(x_list, y_list)

    def __call__(self, x):
        raise NotImplementedError

    def __contains__(self, item):
        return item in self.x_list

    def update(self, x_list=list(), y_list=list()):
        """
        update interpolation data
        :param list(float) x_list: x values
        :param list(float) y_list: y values
        """
        if not y_list:
            for x in x_list:
                if x in self.x_list:
                    i = self.x_list.index(float(x))
                    self.x_list.pop(i)
                    self.y_list.pop(i)
        else:
            x_list = list(map(float, x_list))
            y_list = list(map(float, y_list))
            data = [(x, y) for x, y in zip(self.x_list, self.y_list) if x not in x_list]
            data.extend(list(zip(x_list, y_list)))
            data = sorted(data)
            self.x_list = [float(x) for (x, y) in data]
            self.y_list = [float(y) for (x, y) in data]

    @classmethod
    def from_dict(cls, xy_dict):
        return cls(sorted(xy_dict), (xy_dict[k] for k in sorted(xy_dict)))


class spline(base_interpolation):
    """
    interpolates the data with cubic splines.
    """

    def __init__(self, x_list=list(), y_list=list(), boundary_condition=None):
        """
        :param x_list: data
        :param y_list: data
        :param boundary_condition: Either a tuple (l, r) of values for the slope or None.
            If the argument is not specified then None will be taken as boundary conditions, which
            leads to the so called not-a-knot method for splines. Not-a-knot will determine the boundary conditions by also
            requiring that the third derivatives of the two most left and the two most right interpolation polynomials agree.
            The boundary condition (0,0) will lead to the so called natural spline
            """

        super(spline, self).__init__(x_list, y_list)  # second derivative on the borders is zero
        self.intervals = list()

        self.interpolation_coefficients = list()
        self.boundary_condition = boundary_condition
        for i in range(0, len(self.x_list) - 1):
            self.intervals.append([self.x_list[i], self.x_list[i + 1]])

        if self.y_list:
            self._set_interpolation_coefficients()

    def __call__(self, x):
        """
        returns the interpolated value for the point x.
        :param x:
        :return:
        """
        if not self.y_list:
            raise OverflowError
        ival = spline._get_interval(x, self.intervals)
        i = self.intervals.index(ival)
        t = (x - ival[0]) / (ival[1] - ival[0])
        y = self.y_list
        a = self.interpolation_coefficients[i][0]
        b = self.interpolation_coefficients[i][1]
        return (1 - t) * y[i] + t * y[i + 1] + t * (1 - t) * (a * (1 - t) + b * t)

    @staticmethod
    def _get_interval(x, intervals):
        """
        finds interval of the interpolation in which x lies.
        :param x:
        :param intervals: the interpolation intervals
        :return:
        """
        n = len(intervals)
        if n < 2:
            return intervals[0]
        n2 = int(n / 2)
        if x < intervals[n2][0]:
            return spline._get_interval(x, intervals[:n2])
        else:
            return spline._get_interval(x, intervals[n2:])

    def _set_interpolation_coefficients(self):
        """
        computes the coefficients for the single polynomials of the spline.
        """

        left_boundary_slope = 0
        right_boundary_slope = 0

        if isinstance(self.boundary_condition, tuple):
            left_boundary_slope = self.boundary_condition[0]
            right_boundary_slope = self.boundary_condition[1]
        elif self.boundary_condition is None:
            pass
        else:
            msg = 'The given object {} of type {} is not a valid condition ' \
                  'for the border'.format(self.boundary_condition, type(self.boundary_condition))
            raise ValueError(msg)

        # getting the values such that we get a continuous second derivative
        # by solving a system of linear equations

        # setup the matrix
        n = len(self.x_list)
        mat = [[0. for _ in range(n)] for _ in range(n)]
        b = [[0.] for _ in range(n)]
        x = self.x_list
        y = self.y_list

        if n > 2:
            for i in range(1, n - 1):
                mat[i][i - 1] = 1.0 / (x[i] - x[i - 1])
                mat[i][i + 1] = 1.0 / (x[i + 1] - x[i])
                mat[i][i] = 2 * (mat[i][i - 1] + mat[i][i + 1])

                b[i][0] = 3 * ((y[i] - y[i - 1]) / (x[i] - x[i - 1]) ** 2
                               + (y[i + 1] - y[i]) / (x[i + 1] - x[i]) ** 2)
        elif n < 2:
            raise ValueError('too less points for interpolation')

        if self.boundary_condition is None:  # not a knot
            mat[0][0] = 1.0 / (x[1] - x[0]) ** 2
            mat[0][2] = -1.0 / (x[2] - x[1]) ** 2
            mat[0][1] = mat[0][0] + mat[0][2]

            b[0][0] = 2.0 * ((y[1] - y[0]) / (x[1] - x[0]) ** 3
                             - (y[2] - y[1]) / (x[2] - x[1]) ** 3)

            mat[n - 1][n - 3] = 1.0 / (x[n - 2] - x[n - 3]) ** 2
            mat[n - 1][n - 1] = -1.0 / (x[n - 1] - x[n - 2]) ** 2
            mat[n - 1][n - 2] = mat[n - 1][n - 3] + mat[n - 1][n - 1]

            b[n - 1][0] = 2.0 * ((y[n - 2] - y[n - 3]) / (x[n - 2] - x[n - 3]) ** 3
                                 - (y[n - 1] - y[n - 2]) / (x[n - 1] - x[n - 2]) ** 3)
        else:
            mat[0][0] = 2.0 / (x[1] - x[0])
            mat[0][1] = 1.0 / (x[1] - x[0])

            b[0][0] = 3 * (y[1] - y[0]) / (x[1] - x[0]) ** 2 - 0.5 * left_boundary_slope

            mat[n - 1][n - 2] = 1.0 / (x[n - 1] - x[n - 2])
            mat[n - 1][n - 1] = 2.0 / (x[n - 1] - x[n - 2])

            b[n - 1][0] = 3 * (y[n - 1] - y[n - 2]) / (x[n - 1] - x[n - 2]) ** 2 + 0.5 * right_boundary_slope

        try:
            import numpy
        except ImportError:
            msg = self.__module__, self.__class__.__name__
            raise ImportError('%s.%s requires `numpy` for solving linear equation systems.' % msg)
        k = numpy.linalg.solve(mat, b)

        for i in range(1, n):
            c1 = k[i - 1, 0] * (x[i] - x[i - 1]) - (y[i] - y[i - 1])
            c2 = -k[i, 0] * (x[i] - x[i - 1]) + (y[i] - y[i - 1])
            self.interpolation_coefficients.append([c1, c2])


class natural_spline(spline):
    def __init__(self, x_list=list(), y_list=list()):
        super(natural_spline, self).__init__(x_list, y_list, (0, 0))


class nak_spline(spline):
    def __init__(self, x_list=list(), y_list=list()):
        super(nak_spline, self).__init__(x_list, y_list)
