"""
Application views and routes.
"""

import os.path

import web

from pastetron import db, highlighting


urls = (
    r'/', 'Post',
    r'/(\d+)', 'Show',
    r'/(\d+)/raw', 'ShowRaw',
    r'/pygments.css', 'Stylesheet',
)


render = web.template.render(
    os.path.join(os.path.dirname(__file__), 'templates'),
    base='layout',
    globals={
        'lexers': highlighting.LEXERS,
    }
)


class Post(object):

    def GET(self):
        return render.post()

    def POST(self):
        form = web.input(poster='', syntax='', body='')
        if form.body.strip() == '':
            web.seeother('/')
        if form.syntax == '':
            syntax = highlighting.guess_lexer_alias(form.body)
        else:
            syntax = form.syntax
        paste_id = db.add_paste(form.poster, form.body, syntax)
        web.seeother('/%d' % (paste_id,))


class Show(object):

    def GET(self, paste_id):
        row = db.get_paste(paste_id)
        if row is None:
            return web.notfound('No such paste.')
        formatted = highlighting.highlight(row['body'], row['syntax'])
        return render.paste(
            paste_id=paste_id,
            created=row['created'],
            poster=row['poster'],
            body=formatted,
            syntax=highlighting.ALIAS_TO_NAME[row['syntax']]
        )


class ShowRaw(object):

    def GET(self, paste_id):
        row = db.get_paste(paste_id)
        if row is None:
            return web.notfound('No such paste.')
        return row['body']


class Stylesheet(object):

    def GET(self):
        return highlighting.get_stylesheet()
