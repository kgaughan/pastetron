"""
Pastetron - A pastebin application.
"""

import functools

import web

from pastetron import bootstrap


urls = (
    r'/',
    'pastetron.views.Post',

    r'/(\d+)',
    'pastetron.views.Show',

    r'/chunks/(\d+)',
    'pastetron.views.ShowRaw',

    r'/pastes/(\d+)?',
    'pastetron.views.Recent',

    r'/pygments.css',
    'pastetron.views.Stylesheet',
)

paste = functools.partial(bootstrap.initialise, web.application(urls))

app_factory = functools.partial(bootstrap.initialise_from_environment, paste)
