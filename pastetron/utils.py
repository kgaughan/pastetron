"""
Utility functions.
"""

import sqlite3

import dbkit
import pygments
import pygments.lexers
import pygments.formatters
import web


# for generating the lexers dropdown.
LEXERS = [('Guess', '')] + sorted(
    (longname, aliases[0])
    for longname, aliases, _, _ in pygments.lexers.get_all_lexers()
    if len(aliases) > 0)

# For converting lexer aliases to full names when rendering.
ALIAS_TO_NAME = dict((alias, longname) for longname, alias in LEXERS)

# We'll be reusing this each time something is rendered, so might as well
# create it once.
FORMATTER = pygments.formatters.HtmlFormatter(
    linenos=True,
    cssclass='highlight')


def get_pygments_stylesheet():
    """
    Generate a stylesheet for syntax highlighting the output.
    """
    return FORMATTER.get_style_defs('.highlight')


def guess_lexer_alias(body):
    """
    Guess the alias of the lexer to use when rendering the given text.
    """
    return pygments.lexers.guess_lexer(body).aliases[0]


def highlight(body, format):
    """
    Have Pygments format the given text.
    """
    lexer = pygments.lexers.get_lexer_by_name(format)
    return pygments.highlight(body, lexer, FORMATTER)


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


def initialise(views, global_config, settings):
    """
    Initialises a web.py views views as a WSGI application.
    """
    symbols = dict((k, getattr(views, k)) for k in dir(views))
    app = web.application(views.urls, symbols)
    configure_db_hook(app, global_config, settings)
    return app
