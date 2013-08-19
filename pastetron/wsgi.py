"""
Expose the WSGI application.
"""

from . import paste
from .bootstrap import initialise_from_environment


app = initialise_from_environment(paste)
del initialise_from_environment, paste
