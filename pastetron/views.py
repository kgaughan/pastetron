"""
Application views and routes.
"""

import os.path

import creole
import web

from pastetron import db, highlighting, pagination


urls = (
    r'/', 'Post',
    r'/(\d+)', 'Show',
    r'/(\d+)/raw', 'ShowRaw',
    r'/pastes/(\d+)', 'Index',
    r'/pygments.css', 'Stylesheet',
)


render = web.template.render(
    os.path.join(os.path.dirname(__file__), 'templates'),
    base='layout',
    globals={
        'lexers': highlighting.LEXERS,
        'creole2html': creole.creole2html,
        'paginator': pagination.paginator,
    }
)


class Index(object):

    def GET(self, page_num):
        page_num = int(page_num)
        page_count = db.get_page_count()
        if 0 >= page_num > page_count:
            return web.notfound('No such page.')
        return render.index(
            page_num=page_num,
            page_count=page_count,
            pastes=db.get_paste_list(page_num))


class Post(object):

    def GET(self):
        return render.post()

    def POST(self):
        form = web.input(poster='', title='', syntax='', body='')
        if form.body.strip() == '':
            return web.seeother('/')
        if form.syntax == '':
            syntax = highlighting.guess_lexer_alias(form.body)
        else:
            syntax = form.syntax
        paste_id = db.add_paste(
            form.poster,
            form.title.strip(),
            form.body,
            syntax)
        return web.seeother('/%d' % (paste_id,))


class Show(object):

    def GET(self, paste_id):
        row = db.get_paste(paste_id)
        if row is None:
            return web.notfound('No such paste.')
        title = row['title']
        if title == '':
            title = 'Paste #%s' % paste_id
        formatted = highlighting.highlight(row['body'], row['syntax'])
        comments = db.get_comments(paste_id)
        return render.paste(
            paste_id=paste_id,
            created=row['created'],
            poster=row['poster'],
            title=title,
            body=formatted,
            syntax=highlighting.ALIAS_TO_NAME[row['syntax']],
            comments=comments,
        )

    def POST(self, paste_id):
        form = web.input(poster='', body='')
        if form.body.strip() != '':
            db.add_comment(paste_id, form.poster, form.body)
        return web.seeother('/%s' % (paste_id,))


class ShowRaw(object):

    def GET(self, paste_id):
        row = db.get_paste(paste_id)
        if row is None:
            return web.notfound('No such paste.')
        return row['body']


class Stylesheet(object):

    def GET(self):
        return highlighting.get_stylesheet()
