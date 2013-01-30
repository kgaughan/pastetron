"""
Utility functions.
"""

import sqlite3

import dbkit
import pygments.lexers
import web


# for generating the lexers dropdown.
LEXERS = [('Guess', '')] + sorted(
    (longname, aliases[0])
    for longname, aliases, _, _ in pygments.lexers.get_all_lexers()
    if len(aliases) > 0)


def guess_lexer_alias(body):
    """
    Guess the alias of the lexer to use when rendering the given text.
    """
    return pygments.lexers.guess_lexer(body).aliases[0]


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


def initialise(module, global_config, settings):
    """
    Initialises a web.py application module as a WSGI application.
    """
    symbols = dict((k, getattr(module, k)) for k in dir(module))
    app = web.application(module.urls, symbols)
    configure_db_hook(app, global_config, settings)
    return app
