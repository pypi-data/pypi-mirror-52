
Python library *mathtoolspy*
----------------------------

.. image:: https://img.shields.io/codeship/3c73e880-ba8a-0137-8ad5-4a1d2f2d4303/master.svg
   :target: https://codeship.com//projects/364829
   :alt: CodeShip

.. image:: https://travis-ci.org/sonntagsgesicht/mathtoolspy.svg?branch=master
   :target: https://travis-ci.org/sonntagsgesicht/mathtoolspy
   :alt: Travis ci

.. image:: https://img.shields.io/readthedocs/mathtoolspy
   :target: http://mathtoolspy.readthedocs.io
   :alt: Read the Docs

.. image:: https://img.shields.io/codefactor/grade/github/sonntagsgesicht/mathtoolspy/master
   :target: https://www.codefactor.io/repository/github/sonntagsgesicht/mathtoolspy
   :alt: CodeFactor Grade

.. image:: https://img.shields.io/codeclimate/maintainability/sonntagsgesicht/mathtoolspy
   :target: https://codeclimate.com/github/sonntagsgesicht/mathtoolspy/maintainability
   :alt: Code Climate maintainability

.. image:: https://img.shields.io/codecov/c/github/sonntagsgesicht/mathtoolspy
   :target: https://codecov.io/gh/sonntagsgesicht/mathtoolspy
   :alt: Codecov

.. image:: https://img.shields.io/lgtm/grade/python/g/sonntagsgesicht/mathtoolspy.svg
   :target: https://lgtm.com/projects/g/sonntagsgesicht/mathtoolspy/context:python/
   :alt: lgtm grade

.. image:: https://img.shields.io/lgtm/alerts/g/sonntagsgesicht/mathtoolspy.svg
   :target: https://lgtm.com/projects/g/sonntagsgesicht/mathtoolspy/alerts/
   :alt: total lgtm alerts

.. image:: https://img.shields.io/github/license/sonntagsgesicht/mathtoolspy
   :target: https://github.com/sonntagsgesicht/mathtoolspy/raw/master/LICENSE
   :alt: GitHub

.. image:: https://img.shields.io/github/release/sonntagsgesicht/mathtoolspy?label=github
   :target: https://github.com/sonntagsgesicht/mathtoolspy/releases
   :alt: GitHub release

.. image:: https://img.shields.io/pypi/v/mathtoolspy
   :target: https://pypi.org/project/mathtoolspy/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/mathtoolspy
   :target: https://pypi.org/project/mathtoolspy/
   :alt: PyPI - Python Version

.. image:: https://img.shields.io/pypi/dm/mathtoolspy
   :target: https://pypi.org/project/mathtoolspy/
   :alt: PyPI Downloads

A fast, efficient Python library for mathematically operations, like
integration, solver, distributions and other useful functions.


Example Usage
-------------

.. code-block:: python

    >>> from mathtoolspy.integration import gauss_kronrod

    >>> fct = lambda x:exp(-x*x)
    >>> integrator = gauss_kronrod()
    >>> integrator(fct, -1.0, 2.0)
    1.62890552357

Install
-------

The latest stable version can always be installed or updated via pip:

.. code-block:: bash

    $ pip install mathtoolspy

If the above fails, please try easy_install instead:

.. code-block:: bash

    $ easy_install mathtoolspy


Examples
--------

.. code-block:: python

    # Simplest example possible
	    a, b, c, d, e = 1, 4, -6, -6, 1
        fct = lambda x : a*x*x*x*x + b*x*x*x + c*x*x + d*x + e
        opt = Optimizer1Dim(minimize_algorithm=brent)
        result = opt.optimize(fct, constraint=Constraint(-10.0, -2.0), initila_value=1.0)
        >>> result.xmin
        -3.70107061641
        >>> result.fmin
        -74.1359364077
        >>> result.number_of_function_calls
        40


Development Version
-------------------

The latest development version can be installed directly from GitHub:

.. code-block:: bash

    $ pip install --upgrade git+https://github.com/pbrisk/mathtoolspy.git


Contributions
-------------

.. _issues: https://github.com/pbrisk/mathtoolspy/issues
.. __: https://github.com/pbrisk/mathtoolspy/pulls

Issues_ and `Pull Requests`__ are always welcome.


License
-------

.. __: https://github.com/pbrisk/mathtoolspy/raw/master/LICENSE

Code and documentation are available according to the Apache Software License (see LICENSE__).


