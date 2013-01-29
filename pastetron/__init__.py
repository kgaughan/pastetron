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
    app = pastetron.utils.initialise(pastetron.app, global_config, settings)
    return app.wsgifunc()
