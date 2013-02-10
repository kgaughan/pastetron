"""
Various utility functions.
"""

import mimeparse
import web


def get_preferred_mimetype(acceptable, default):
    """
    Gets the preferred MIME type to use for rendering the response based on
    what the client will accept.
    """
    if 'HTTP_ACCEPT' not in web.ctx.env:
        return default
    return mimeparse.best_match(acceptable, web.ctx.env['HTTP_ACCEPT'])
