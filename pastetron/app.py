"""
"""

import os.path

import web

from pastetron import db, utils


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

    def POST(self):
        form = web.input(poster='', format='', body='')
        if form.body.strip() == '':
            web.seeother('/')
        if form.format == '':
            format = utils.guess_lexer_alias(form.body)
        else:
            format = form.format
        paste_id = db.add_paste(form.poster, form.body, format)
        web.seeother('/%d' % (paste_id,))
