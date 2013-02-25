"""
A reCAPTCHA_ client library.

.. _reCAPTCHA: http://www.google.com/recaptcha

Copyright (c) Keith Gaughan, 2013.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from __future__ import with_statement

import contextlib
import urllib
import urllib2


__all__ = (
    'make_markup',
    'check',
)

__version__ = '0.1.0'
__author__ = 'Keith Gaughan'
__email__ = 'k@stereochro.me'


MARKUP = """
<script type="text/javascript"
 src="//www.google.com/recaptcha/api/challenge?%(params)s"></script>
<noscript>
<iframe src="//www.google.com/recaptcha/api/noscript?%(params)s"
 height="300" width="500" frameborder="0"></iframe><br>
<textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
<input type="hidden" name="recaptcha_response_field" value="manual_challenge">
</noscript>
""".replace("\n", "")


def make_markup(public_key, error=None):
    """
    Generate the HTML to display the CAPTCHA.
    """
    keys = {'k': public_key}
    if error is not None:
        keys['error'] = error
    return MARKUP % {'params': urllib.urlencode(keys)}


def check(private_key, remote_ip, challenge, response):
    """
    Validate the CAPTCHA response.
    """
    if challenge.strip() == '' or response.strip() == '':
        return (False, 'incorrect-captcha-sol')

    params = {
        'privatekey': private_key,
        'remoteip': remote_ip,
        'challenge': challenge,
        'response': response,
    }
    fh = urllib2.urlopen(
        'http://www.google.com/recaptcha/api/verify',
        urllib.urlencode(params))
    with contextlib.closing(fh):
        response = fh.read().splitlines()
        if response[0] == 'false':
            return (False, response[1])
        return (True, '')
