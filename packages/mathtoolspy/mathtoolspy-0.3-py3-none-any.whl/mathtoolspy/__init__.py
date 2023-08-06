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


import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())


__doc__ = 'A fast, efficient Python library for mathematically operations, ' \
          'like integration, solver, distributions and other useful functions.'
__version__ = '0.3'
__dev_status__ = '4 - Beta'
__date__ = 'Wednesday, 18 September 2019'
__author__ = 'sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]'
__email__ = 'sonntagsgesicht@icloud.com'
__url__ = 'https://github.com/sonntagsgesicht/' + __name__
__license__ = 'Apache License 2.0'
__dependencies__ = ()
__dependency_links__ = ()
__data__ = ()
__scripts__ = ()


from .distribution import *
from .integration import *
from .interpolation import *
from .solver import *
from .utils import *
