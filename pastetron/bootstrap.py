"""
Application bootstrapping.
"""

import sqlite3

import dbkit
import web

from pastetron import utils


def configure_db_hook(app, global_config, settings):
    """
    Ensure each request is done in a properly configured database context.
    """
    path = settings.get('db_path', '%(here)s/pastetron.db') % global_config
    pool = dbkit.create_pool(sqlite3, 10, path)
    pool.default_factory = dbkit.dict_set

    def request_processor(handler):
        """
        Do anything that needs to be done at the beginning and end of a
        request here.
        """
        with pool.connect():
            return handler()
    app.add_processor(request_processor)


def configure_authentication(views, settings):
    """
    """
    auth_method_name = settings.get('auth_method', 'pastetron.httpauth:DUMMY')
    views.auth.method = utils.load_object(auth_method_name)
    views.auth.realm = settings.get('auth_realm', 'Pastetron')


def initialise(views, global_config, settings):
    """
    Initialises a web.py views views as a WSGI application.
    """
    symbols = dict((k, getattr(views, k)) for k in dir(views))
    web.config.app = web.Storage(**settings)
    app = web.application(views.urls, symbols)
    configure_db_hook(app, global_config, settings)
    configure_authentication(views, settings)
    return app
