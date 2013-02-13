"""
Various utility functions.
"""

import datetime

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


def date(timestamp, fmt=None, tz=None):
    """
    Formatting of SQLite timestamps.

    SQLite timestamps are taken to be in UTC. If you want them adjusted to
    another timezone, pass a `tzinfo` object representing that timezone in
    the `tz` parameter. The `fmt` parameter specifies a `strftime` date format
    string; it defaults to the `ISO 8601`_/`RFC 3339`_ date format.

    .. _ISO 8601: http://en.wikipedia.org/wiki/ISO_8601
    .. _RFC 3339: http://tools.ietf.org/html/rfc3339
    """
    if fmt is None:
        fmt = '%Y-%m-%dT%H:%M:%S' + ('Z' if tz is None else '%z')
    dt = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    if tz is not None:
        dt = dt.astimezone(tz)
    return dt.strftime(fmt)


def get_poster():
    """
    Gets the poster name from a cookie.
    """
    return web.cookies(poster='Anonymous').poster


def save_poster(poster):
    """
    Save the given poster name for seven days.
    """
    seven_days = 60 * 60 * 24 * 7
    web.setcookie('poster', poster, expires=seven_days)
