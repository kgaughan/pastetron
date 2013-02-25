"""
Pastetron - A pastebin application.
"""

import pastetron.bootstrap
import pastetron.views
# pylint: disable-msg=W0401
from pastetron.version import *  # flake8: noqa


def paste(global_config, **settings):
    """
    PasteDeploy runner.
    """
    app = pastetron.bootstrap.initialise(
        pastetron.views,
        global_config,
        settings)
    return app.wsgifunc()
