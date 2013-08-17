"""
Pastetron - A pastebin application.
"""

import functools

import web

import pastetron.bootstrap


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

app_factory = functools.partial(pastetron.bootstrap.initialise,
                                web.application(urls))
