"""
Atom feed generation.
"""

from __future__ import with_statement

import contextlib
try:
    import xml.etree.cElementTree as et
except:  # pylint: disable-msg=W0702
    import xml.etree.ElementTree as et

import web

from pastetron import version, utils


@contextlib.contextmanager
def nesting(tb, tag_, **attrs):
    """
    Generates an element containing nested elements within the given
    `TreeBuilder` stream.
    """
    tb.start(tag_, attrs)
    yield
    tb.end(tag_)


def tag(tb, tag_, *values, **attrs):
    """
    Generates a simple element in the given `TreeBuilder` stream.
    """
    tb.start(tag_, attrs)
    for value in values:
        tb.data(value)
    tb.end(tag_)


def generate_feed(entries):
    """
    Generate an Atom feed.
    """
    tb = et.TreeBuilder()
    build_feed(
        tb,
        web.config.app.title,
        'now',
        web.config.app.tag_uri,
        entries)
    return et.tostring(tb.close(), 'UTF-8')


def build_feed(tb, title, updated, id_, entries):
    """
    Build an Atom feed. Requires a `TreeBuilder` to build the feed with.
    """
    with nesting(tb, 'feed', xmlns='http://www.w3.org/2005/Atom'):
        tag(tb, 'title', title)
        tag(tb, 'link', href=web.ctx.realhome + '/pastes/', rel='self')
        tag(tb, 'link', href=web.ctx.realhome + '/', rel='alternate')
        tag(tb, 'updated', updated)
        tag(tb, 'id', id_)
        tag(
            tb, 'generator', 'Pastetron',
            uri='https://github.com/kgaughan/pastetron',
            version=version.__version__)
        for entry in entries:
            build_entry(tb, id_, entry)


def build_entry(tb, id_, entry):
    """
    Build an Atom feed entry.
    """
    with nesting(tb, 'entry'):
        tag(tb, 'title', entry['title'])
        link = '%s/%d' % (web.ctx.realhome, entry['paste_id'])
        tag(tb, 'link', rel='alternate', type='text/html', href=link)
        tag(tb, 'id', '%s:p%d' % (id_, entry['paste_id']))
        tag(tb, 'published', entry['created'])
        tag(tb, 'updated', entry['created'])
        with nesting(tb, 'author'):
            tag(tb, 'name', entry['poster'])
        tag(tb, 'content', entry['body'], type='text')
