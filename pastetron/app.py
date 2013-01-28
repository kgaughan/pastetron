"""
"""

import os.path

import web


urls = (
    '/', 'List',
)


render = web.template.render(
    os.path.join(os.path.dirname(__file__), 'templates'),
    base='layout',
    globals={})


class List(object):

    def GET(self):
        return render.index()
