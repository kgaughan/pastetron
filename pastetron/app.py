"""
"""

import os.path

import web


urls = (
    # List recent pastes; add new paste.
    '/', 'Root',
)


render = web.template.render(
    os.path.join(os.path.dirname(__file__), 'templates'),
    base='layout',
    globals={})


class Root(object):

    def GET(self, action):
        return render.index('We now have template rendering.')
