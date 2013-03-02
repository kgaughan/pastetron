"""
HTTP authentication support for web.py
"""

import base64
import functools
import hashlib
import math
import os
import re
import time

import web


__all__ = (
    'make_hash', 'join_fields', 'parse_fields',
    'Auth', 'DigestAuth',
    'DUMMY', 'FORWARDED_USER', 'BASIC', 'DIGEST',
    'AuthMediator',
)


class StaleAuth(Exception):
    """
    The authorisation details provided were stale.
    """


PARSE_HEADER = re.compile(r'''(\w+)=(?:(['"])([^'"]*)\2|([^\s,]*))''')


def make_hash(fields, delimiter=':'):
    """
    Hashes a bunch of fields separated by a delimiter.
    """
    return hashlib.md5(delimiter.join(fields)).hexdigest()


def join_fields(fields):
    """
    Join a bunch of key/value pairs together.
    """
    return ', '.join('%s="%s"' % pair for pair in fields.iteritems())


def parse_fields(header):
    """
    Parse the comma-separated fields from a header.
    """
    for match in PARSE_HEADER.finditer(header):
        key = match.group(1).lower()
        value = match.group(3)
        if value == '':
            value = match.group(4)
        yield key, value


def _get_header():
    """
    Get the value of the HTTP Authorization header, if present.
    """
    header = web.ctx.env.get('HTTP_AUTHORIZATION')
    if header is None:
        return None, None
    parts = header.split(' ', 1)
    if len(parts) == 1:
        parts.append('')
    return parts[0], parts[1]


def send_header(method, fields):
    """
    Send a WWW-Authenticate header.
    """
    web.ctx.status = '401 Unauthorized'
    header = '%s %s' % (method.name, join_fields(fields))
    web.header('WWW-Authenticate', header)


class Auth(object):
    """
    Base class for authentication methods.
    """

    name = None

    expected = ()

    def challenge(self, realm, stale):
        """
        Issue a HTTP auth challenge.
        """
        pass

    def parse_header(self, data):
        """
        Extract the fields from an Authorization header.

        Returns a tuple consisting of the username followed by a dict of any
        additional parameters present.
        """
        missing = set(self.expected)
        fields = {}
        for key, value in parse_fields(data):
            if key in missing:
                fields[key] = value
                missing.remove(key)
        if len(missing) > 0:
            raise ValueError('Missing fields: %s' % ', '.join(missing))
        return fields['username'], fields

    def check(self, data, headers, mediator):
        """
        Check the provided auth information.

        `data` is the contents of the 'Authorization' header after the method
        name, `headers` is a dict of the request headers (in case this method
        requires access to additional headers), and `mediator`, which can be
        called to check that the
        """
        raise NotImplementedError


class _DummyAuth(Auth):
    """
    A dummy authentication method that always succeeds.
    """

    def check(self, data, headers, mediator):
        return headers.get('REMOTE_USER', None), True


class _ForwardedUserAuth(Auth):
    """
    A dummy authentication method that always if the 'X-Forwarded-User'
    header is set. This is useful if your app runs behind a reverse proxy
    that handles auth itself.
    """

    def challenge(self, realm, stale):
        web.ctx.status = '403 Forbidden'


    def check(self, data, headers, mediator):
        username = headers.get('HTTP_X_FORWARDED_USER', None)
        return username, mediator.is_valid_username(username)


class _BasicAuth(Auth):
    """
    Implements HTTP Basic authentication.
    """

    name = 'Basic'

    def challenge(self, realm, stale):
        send_header(self, {'realm': realm})

    def check(self, data, headers, mediator):
        try:
            username, password = base64.b64decode(data).split(':', 1)
        except (TypeError, ValueError):
            return None, False
        if mediator.check_basic_credentials(username, password):
            return username, True
        return None, False


class DigestAuth(Auth):
    """
    Implements HTTP digest authentication (only RFC 2069 for now).
    """

    name = 'Digest'

    expected = ('username', 'nonce', 'username', 'uri', 'response')

    def __init__(self, lifetime=60):
        super(DigestAuth, self).__init__()
        self.lifetime = lifetime
        self.private_key = base64.b64encode(os.urandom(256))
        self.time = time.time

    def challenge(self, realm, stale):
        send_header(self, {
            'realm': realm,
            'nonce': self._make_nonce(web.ctx.ip),
            'stale': 'true' if stale else 'false',
        })

    @staticmethod
    def make_ha1(username, realm, password):
        """
        Make a HA1 hash (username + realm + password)
        """
        return make_hash((username, realm, password))

    @staticmethod
    def make_response(ha1, nonce, ha2):
        """
        Make a response hash (ha1 + nonce + ha2)
        """
        return make_hash((ha1, nonce, ha2))

    def _make_nonce(self, remote_ip):
        """
        Generate a suitable nonce value.
        """
        fields = (
            str(math.trunc(self.time() / self.lifetime)),
            remote_ip,
            self.private_key,
        )
        return make_hash(fields, delimiter='|')

    def check(self, data, headers, mediator):
        try:
            username, fields = self.parse_header(data)
        except ValueError:
            return None, False

        ha1 = mediator.get_digest_ha1(username)
        if ha1 is None:
            return None, False

        nonce = self._make_nonce(web.ctx.ip)
        if nonce != fields['nonce']:
            raise StaleAuth
        ha2 = make_hash((web.ctx.method, fields['uri']))
        expected = self.make_response(ha1, nonce, ha2)
        return username, fields['response'] == expected


# Default dummy auth checker.
DUMMY = _DummyAuth()
# Default forwarded user auth checker.
FORWARDED_USER = _ForwardedUserAuth()
# Default basic auth checker.
BASIC = _BasicAuth()
# Default digest auth checker.
DIGEST = DigestAuth()


class AuthMediator(object):
    """
    Handles checking the auth header against various authentication methods.
    """

    def __init__(self, method=DUMMY, realm='Web'):
        super(AuthMediator, self).__init__()
        self.realm = realm
        self.method = method

    # pylint: disable=W0613,R0201
    def check_basic_credentials(self, username, password):
        """
        Check the given set of credentials against an authentication source.
        """
        return False

    # pylint: disable=R0201
    def get_digest_ha1(self, username):
        """
        Given a username, get the corresponding Digest HA1 hash.
        Returns `None` if no record is associated with the username.
        """
        return None

    # pylint: disable=W0613,R0201
    def check_wsse_credentials(self, username, digest, timestamp, nonce):
        """
        Check the given set of credentials against an authentication source.
        """
        return False

    # pylint: disable=R0201
    def is_valid_username(self, username):
        return False

    # pylint: disable=R0201
    def default_response(self):
        """
        Called when access is made without authentication.
        """
        return 'Unauthorised access denied'

    def _is_authorized(self):
        """
        Check if the provided credentials match.
        """
        auth_type = None
        auth_data = None
        if self.method.name is not None:
            auth_type, auth_data = _get_header()

        # Unexpected auth type.
        if self.method.name != auth_type:
            return False

        username, authorized = self.method.check(auth_data, web.ctx.env, self)
        if username is not None:
            web.ctx.env['REMOTE_USER'] = username
        return authorized

    def requires_auth(self, func):
        """
        Decorates a view method as requiring authorisation to run.

        If successful, `web.ctx.env['REMOTE_USER']` will contain the
        authenticated user's username.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):  # pylint: disable=C0111
            try:
                authorized = self._is_authorized()
                stale = False
            except StaleAuth:
                authorized = False
                stale = True
            if authorized:
                return func(*args, **kwargs)
            self.method.challenge(realm=self.realm, stale=stale)
            return self.default_response()
        return wrapper
