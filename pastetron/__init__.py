"""
Pastetron - A pastebin application.
"""

import pastetron.app
import pastetron.utils


__version__ = '0.1.0'
__author__ = 'Keith Gaughan'
__email__ = 'k@stereochro.me'


def paste(global_config, **settings):
    """
    PasteDeploy runner.
    """
    return pastetron.utils.initialise(pastetron.app, settings).wsgifunc()
