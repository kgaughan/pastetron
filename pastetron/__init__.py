"""
Pastetron - A pastebin application.
"""

import sqlite3

import dbkit
import web

import pastetron.app


__version__ = '0.1.0'
__author__ = 'Keith Gaughan'
__email__ = 'k@stereochro.me'


def configure_db_hook(app, settings):
    """
    Ensure each request is done in a properly configured database context.
    """
    pool = dbkit.create_pool(
        sqlite3, 10,
        settings.get('db_path', '/tmp/pastetron.db'))
    pool.default_factory = dbkit.dict_set

    def request_processor(handler):
        """
        Do anything that needs to be done at the beginning and end of a
        request here.
        """
        with pool.connect():
            return handler()
    app.add_processor(request_processor)


def initialise(module, settings):
    """
    Initialises a web.py application module as a WSGI application.
    """
    symbols = dict((k, getattr(module, k)) for k in dir(module))
    app = web.application(module.urls, symbols)
    configure_db_hook(app, settings)
    return app


def paste(global_config, **settings):
    """
    PasteDeploy runner.
    """
    return initialise(pastetron.app, settings).wsgifunc()
