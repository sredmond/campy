# Set default logging handler to avoid "No handler found" warnings.
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = "Sam Redmond"
__copyright__ = "Copyright 2016-2019"
__credits__ = ["Sam Redmond", "Alex Valderrama", "Marty Stepp", "Eric Roberts"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Sam Redmond"
__email__ = "sredmond@stanford.edu"
__status__ = "Prototype"

