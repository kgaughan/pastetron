"""
Application views and routes.
"""

import functools
import os.path

import creole
import web

from pastetron import db, feed, highlighting, pagination, utils


urls = (
    r'/', 'Post',
    r'/(\d+)', 'Show',
    r'/(\d+)/raw', 'ShowRaw',
    r'/pastes/(\d+)?', 'Recent',
    r'/pygments.css', 'Stylesheet',
)


render = web.template.render(
    os.path.join(os.path.dirname(__file__), 'templates'),
    base='layout',
    globals={
        'get_site_name': utils.get_site_name,
        'creole2html': creole.creole2html,
        'lexers': highlighting.LEXERS,
        'paginator': pagination.paginator,
        'url': web.url,
        'date': utils.date,
        'human': functools.partial(utils.date, fmt='%B %d, %Y at %H:%M'),
        'captcha': utils.make_captcha_markup,
        'highlight': highlighting.highlight,
    }
)


class Recent(object):
    """
    Index of all pastes, from most recent to oldest.
    """

    def GET(self, page_num=None):
        mime_type = utils.get_preferred_mimetype(
            ('text/html', 'application/atom+xml'),
            'text/html')
        if mime_type == 'text/html':
            if page_num is None:
                return web.seeother(web.url('/pastes/1'))
            return self.recent(int(page_num))
        if mime_type == 'application/atom+xml':
            return self.feed()
        # Should never be called.
        return web.notacceptable()

    def recent(self, page_num):
        """
        Render the HTML form of the index.
        """
        page_count = db.get_page_count()
        if 0 >= page_num > page_count:
            return web.notfound('No such page.')
        return render.recent(
            page_num=page_num,
            page_count=page_count,
            pastes=db.get_paste_list(page_num))

    def feed(self):
        response = feed.generate_feed(db.get_latest_pastes())
        if response is None:
            return web.notfound('No feed.')
        web.header(
            'Content-Type',
            'application/atom+xml; charset=utf-8',
            unique=True)
        return response


class Post(object):
    """
    Form for posting up a new paste.
    """

    def GET(self):
        return render.post(user=utils.get_poster())

    def POST(self):
        form = web.input(
            poster=utils.get_default_name(),
            title='',
            syntax='text',
            body='',
            do_preview=None,
        )
        is_valid, error = utils.check_captcha(web.ctx['ip'], form)
        if not is_valid or form.do_preview is not None:
            return render.post(
                user=form.poster,
                title=form.title,
                syntax=form.syntax,
                body=form.body,
                captcha_error=error,
                preview=form.do_preview is not None,
            )
        utils.save_poster(form.poster)
        if form.body.strip() == '':
            return web.seeother(web.url('/'))
        paste_id = db.add_paste(
            form.poster,
            form.title.strip(),
            form.body,
            form.syntax,
        )
        return web.seeother(web.url('/%d' % (paste_id,)))


class Show(object):
    """
    Show a paste and post comments on the paste.
    """

    def GET(self, paste_id):
        return self.show_paste(paste_id)

    def show_paste(self, paste_id, comment='', captcha_error=None):
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
            body=row['body'],
            syntax=row['syntax'],
            comments=comments,
            user=utils.get_poster(),
            comment=comment,
            captcha_error=captcha_error,
        )

    def POST(self, paste_id):
        form = web.input(
            poster=utils.get_default_name(),
            body='')
        is_valid, captcha_error = utils.check_captcha(web.ctx['ip'], form)
        if not is_valid:
            return self.show_paste(paste_id, form.body, captcha_error)
        utils.save_poster(form.poster)
        if form.body.strip() != '':
            db.add_comment(paste_id, form.poster, form.body)
        return web.seeother('/%s' % (paste_id,))


class ShowRaw(object):
    """
    Show a raw paste.
    """

    def GET(self, paste_id):
        row = db.get_paste(paste_id)
        if row is None:
            return web.notfound('No such paste.')
        web.header('Content-Type', 'text/plain; charset=utf-8', unique=True)
        return row['body']


class Stylesheet(object):
    """
    Generate the Pygments stylesheet.
    """

    def GET(self):
        web.header('Content-Type', 'text/css; charset=utf-8', unique=True)
        return highlighting.get_stylesheet()
