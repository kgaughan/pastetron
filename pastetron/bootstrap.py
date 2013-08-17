"""
Application bootstrapping.
"""

import sqlite3

import dbkit
import web

from pastetron import utils, views


def initialise(app, global_config=None, **settings):
    """
    Initialise a web.py application, returning a WSGI application.
    """
    if global_config is None:
        global_config = {
            'here': '.',
        }

    # Defaults.
    settings.setdefault('db_path', '%(here)s/pastetron.db' % global_config)
    settings.setdefault('auth_method', 'pastetron.httpauth:DUMMY')
    settings.setdefault('auth_realm', 'Pastetron')

    # Allow the application access to the configuration.
    web.config.app = web.Storage(**settings)

    # Ensure each request is done in a properly configured database context.
    pool = dbkit.create_pool(sqlite3, 10, settings['db_path'])
    pool.default_factory = dbkit.dict_set

    def request_processor(handler):
        """
        Do anything that needs to be done at the beginning and end of a
        request here.
        """
        with pool.connect():
            return handler()

    app.add_processor(request_processor)

    # Authentication.
    views.auth.method = utils.load_object(settings['auth_method'])
    views.auth.realm = settings['auth_realm']

    return app.wsgifunc()
