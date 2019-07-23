"""
CAMPY Graphics Library
~~~~~~~~~~~~~~~~~~~~~~

The campy library makes Stanford's graphical ACM libraries available in Python.

# TODO(sredmond): Add basic usage examples.

Full documentation is available at <https://campy.sredmond.io/>

:copyright: (c) 2016-2019 by Sam Redmond.
:license: MIT License. See LICENSE for more details.
"""
import warnings

# TODO(sredmond): Check compatibility of dependency versions.

# TODO(sredmond): Check backend availability.
try:
    import _tkinter
except ImportError as err:
    warnings.warn('Unable to find _tkinter library. If using the Tk backend, you will need to install a version of Python with Tk support.')

try:
    import tkinter
except ImportError as err:
    warnings.warn('Unable to find tkinter library. If using the Tk backend, you will need to install a version of Python with Tk support.')

# Import package metadata.
from .__version__ import (
    __title__, __description__, __url__, __license__,
    __version__, __build__, __status__, __author__,
    __maintainer__, __email__, __copyright__, __credits__,
    __snake__
)

# OPTIONAL(sredmond): Import subpackages to the top-level namespace.

# Set default logging handler to avoid "No handler found" warnings.
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())  # Add a default do-nothing handler to these logs.

# TODO(sredmond): FOR DEVELOPMENT ONLY. Log all messages.
import os
if os.environ.get('CAMPY_DEVELOP'):
    default_log_level = 'DEBUG'
else:
    default_log_level = 'WARNING'
level = os.environ.get('CAMPY_LOGLEVEL', default_log_level).upper()

logging.basicConfig()
logger.setLevel(level)
# Send some initial messages.
logger.info("Welcome to the campy libraries.")
logger.info("If you have any questions, reach out to {me} at {email}".format(me=__maintainer__, email=__email__))
