"""
"""

import os.path

import web

from pastetron import utils


urls = (
    '/', 'Post',
)


render = web.template.render(
    os.path.join(os.path.dirname(__file__), 'templates'),
    base='layout',
    globals={
        'lexers': utils.LEXERS,
    }
)


class Post(object):

    def GET(self):
        return render.post()
