"""
Application bootstrapping.
"""

import sqlite3

import dbkit
import web

from pastetron import utils, views


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


def configure_authentication(settings):
    """
    """
    auth_method_name = settings.get('auth_method', 'pastetron.httpauth:DUMMY')
    views.auth.method = utils.load_object(auth_method_name)
    views.auth.realm = settings.get('auth_realm', 'Pastetron')


def initialise(app, global_config, **settings):
    """
    Initialise a web.py application, returning a WSGI application.
    """
    web.config.app = web.Storage(**settings)
    configure_db_hook(app, global_config, settings)
    configure_authentication(settings)
    return app.wsgifunc()
