"""
Pastetron - A pastebin application.
"""

import functools

import web

from . import bootstrap


urls = (
    r'/',
    'pastetron.views.Post',

    r'/(\d+)',
    'pastetron.views.Show',

    r'/chunks/(\d+)',
    'pastetron.views.ShowRaw',

    r'/pastes/(\d+)?',
    'pastetron.views.Recent',
)

paste = functools.partial(bootstrap.initialise, web.application(urls))
