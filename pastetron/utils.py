"""
Various utility functions.
"""

import contextlib
import datetime
from xml.sax import saxutils

import mimeparse
import web

from pastetron import recaptcha


class XMLBuilder(object):
    """
    Generates an XML document.
    """

    def __init__(self, out, encoding='utf-8'):
        self.generator = saxutils.XMLGenerator(out, encoding)
        self.generator.startDocument()

    @contextlib.contextmanager
    def within(self, tag, **attrs):
        """
        Generates an element containing nested elements.
        """
        self.generator.startElement(tag, attrs)
        yield
        self.generator.endElement(tag)

    def tag(self, tag, *values, **attrs):
        """
        Generates a simple element.
        """
        self.generator.startElement(tag, attrs)
        for value in values:
            self.generator.characters(value)
        self.generator.endElement(tag)


def get_default_name():
    """
    Get the site name from the configuration.
    """
    return web.config.app.get('default_author', 'Anonymous')


def get_site_name():
    """
    Get the site name from the configuration.
    """
    return web.config.app.get('site_name', 'Pastetron:')


def get_page_length():
    """
    Get number of items to display per page.
    """
    return int(web.config.app.get('pastes_per_page', 20))


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
    return web.cookies(poster=get_default_name()).poster


def save_poster(poster):
    """
    Save the given poster name for seven days.
    """
    seven_days = 60 * 60 * 24 * 7
    web.setcookie('poster', poster, expires=seven_days)


def make_captcha_markup(error=None):
    """
    reCAPTCHA wrapper: generate CAPTCHA markup.
    """
    if 'recaptcha_public_key' not in web.config.app:
        return ''
    return recaptcha.make_markup(web.config.app.recaptcha_public_key, error)


def check_captcha(remote_ip, fields):
    """
    reCAPTCHA wrapper: check the CAPTCHA response.
    """
    # If reCAPTCHA support isn't enabled, it always validates.
    if 'recaptcha_private_key' not in web.config.app:
        return (True, '')
    return recaptcha.check(
        web.config.app.recaptcha_private_key,
        remote_ip,
        fields.get('recaptcha_challenge_field', ''),
        fields.get('recaptcha_response_field', ''))
