"""
Pastetron - A pastebin application.
"""

import pastetron.bootstrap
import pastetron.views
from pastetron.version import *  # pylint: disable-msg=W0401


def paste(global_config, **settings):
    """
    PasteDeploy runner.
    """
    app = pastetron.bootstrap.initialise(
        pastetron.views,
        global_config,
        settings)
    return app.wsgifunc()
