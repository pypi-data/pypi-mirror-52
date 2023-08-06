"""
.. include:: ../../README.md
"""

from collections import namedtuple

__title__ = 'dataclasses-config'
__author__ = 'Peter Zaitcev / USSX Hares'
__license__ = 'BSD 2-clause'
__copyright__ = 'Copyright 2019 Peter Zaircev'
__version__ = '0.1.0'


VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(major=0, minor=0, micro=3, releaselevel='alpha', serial=0)

from ._classes import *
from ._config import *
from ._decorations import *

__all__ =  \
[
    'version_info',
    '__title__',
    '__author__',
    '__license__',
    '__copyright__',
    '__version__',
]

_all = \
[
    _classes.__all__,
    _config.__all__,
    _decorations.__all__,
]

for _dep in _all:
    __all__.extend(_dep)
