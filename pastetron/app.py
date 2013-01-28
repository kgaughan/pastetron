"""
"""


import web


urls = (
    # List recent pastes; add new paste.
    '/', 'Root',
)


render = web.template.render('templates', base='layout', globals={})


class Root(object):

    def GET(self):
        return 'You are being served!'
