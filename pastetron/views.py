"""
Application views and routes.
"""

import os.path

import web

from pastetron import db, utils


urls = (
    '/', 'Post',
    '/(\d+)', 'Show',
    '/(\d+)/raw', 'ShowRaw',
    '/pygments.css', 'Stylesheet',
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


class Show(object):

    def GET(self, paste_id):
        row = db.get_paste(paste_id)
        if row is None:
            return web.notfound('No such paste.')
        formatted = utils.highlight(row['body'], row['format'])
        return render.paste(
            paste_id=paste_id,
            created=row['created'],
            poster=row['poster'],
            body=formatted,
            format=utils.ALIAS_TO_NAME[row['format']]
        )


class ShowRaw(object):

    def GET(self, paste_id):
        row = db.get_paste(paste_id)
        if row is None:
            return web.notfound('No such paste.')
        return row['body']


class Stylesheet(object):

    def GET(self):
        return utils.get_pygments_stylesheet()
