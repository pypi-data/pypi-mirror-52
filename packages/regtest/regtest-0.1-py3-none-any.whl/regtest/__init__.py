# -*- coding: utf-8 -*-

# regtest
# -------
# regression test enhancement for the Python unittest framework.
# 
# Author:   sonntagsgesicht
# Version:  0.1, copyright Wednesday, 18 September 2019
# Website:  https://github.com/sonntagsgesicht/regtest
# License:  Apache License 2.0 (see LICENSE file)


import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())


__doc__ = 'regression test enhancement for the Python unittest framework.'
__version__ = '0.1'
__dev_status__ = '4 - Beta'
__date__ = 'Wednesday, 18 September 2019'
__author__ = 'sonntagsgesicht'
__email__ = 'sonntagsgesicht@icloud.com'
__url__ = 'https://github.com/sonntagsgesicht/' + __name__
__license__ = 'Apache License 2.0'
__dependencies__ = ()
__dependency_links__ = ()
__data__ = ()
__scripts__ = ()


from unittest import *
from .regtest import RegressionTestCase
