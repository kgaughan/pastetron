"""
Authorisation.
"""

import dbkit

from . import httpauth


class AuthMediator(httpauth.AuthMediator):
    """
    Auth.

    Passwords are stored as A1 hashes.
    """

    def get_digest_ha1(self, username):
        return dbkit.query_value("""
            SELECT   password
            FROM     users
            WHERE    username = ?
            """, (username,))
