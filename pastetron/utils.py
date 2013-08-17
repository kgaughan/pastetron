"""
Various utility functions.
"""

import ConfigParser
import contextlib
import datetime
import os
import re
from xml.sax import saxutils

import mimeparse
import web

from . import recaptcha


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


def to_page_count(n_entries, entries_per_page):
    """
    Calculate the number of pages given a page count.
    """
    if n_entries == 0:
        return 0
    # How this works:
    # Say the number of entries per page was 10. Thus we'd want entries 1-10
    # to appear on page 1, 11-20 to appear on page 2, and so on. Naively, the
    # number of pages is `n_entries / entries_per_page`, but as we're using
    # integer arithmetic, this rounds down, so we need to adjust it up one.
    # Also, if the number of entries is divisible by the number of page, (e.g.
    # there are ten entries), the naive arithmetic will end up stating there
    # are two pages, not just one. Thus to compensate for that, we subtract
    # one from the number of entries before dividing.
    return ((n_entries - 1) / entries_per_page) + 1


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


OBJECT_REF_PATTERN = re.compile(r"""
    ^
    (?P<module>
        [a-z_][a-z0-9_]*(?:\.[a-z_][a-z0-9_]*)*
    )
    :
    (?P<object>
        [a-z_][a-z0-9_]*
    )
    $
    """, re.I | re.X)


def load_object(object_ref):
    """
    Attempts to import the named object. The object reference is a name in
    the form 'module.name:object_name'.
    """
    matches = OBJECT_REF_PATTERN.match(object_ref)
    if not matches:
        raise ValueError("Malformed object reference: '%s'" % object_ref)

    module_name = matches.group('module')
    object_name = matches.group('object')

    module = __import__(module_name, fromlist=[object_name])
    return getattr(module, object_name)


def read_configuration(env_var, section):
    """
    Read a section from an INI file pointed to by an environment variable.
    """
    config = ConfigParser.RawConfigParser()
    config.add_section(section)
    path = os.getenv(env_var)
    if path is not None:
        config.read(path)
    return dict(config.items(section))
