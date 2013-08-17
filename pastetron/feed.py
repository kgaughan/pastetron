"""
Atom feed generation.
"""

from __future__ import with_statement

import contextlib
try:
    import cStringIO as stringio
except:  # pylint: disable-msg=W0702
    import StringIO as stringio

import pkg_resources
import web

from . import utils


def generate_feed(entries):
    """
    Generate an Atom feed.
    """
    entries = list(entries)
    if len(entries) == 0:
        return None

    # Get the update date. Assumption: most recent entry is first.
    updated = entries[0]['created']

    with contextlib.closing(stringio.StringIO()) as out:
        builder = utils.XMLBuilder(out)
        build_feed(
            builder,
            web.config.app.site_name,
            updated,
            web.config.app.tag_uri,
            entries)
        return out.getvalue()


def build_feed(builder, title, updated, id_, entries):
    """
    Build an Atom feed. Requires an `XMLBuilder` to build the feed with.
    """
    with builder.within('feed', xmlns='http://www.w3.org/2005/Atom'):
        builder.tag('title', title)
        builder.tag('link', href=web.ctx.realhome + '/pastes/', rel='self')
        builder.tag('link', href=web.ctx.realhome + '/', rel='alternate')
        builder.tag('updated', utils.date(updated))
        builder.tag('id', id_)
        builder.tag(
            'generator', 'Pastetron',
            uri='https://github.com/kgaughan/pastetron',
            version=pkg_resources.get_distribution('pastetron').version,
        )
        for entry in entries:
            build_entry(builder, id_, entry)


def build_entry(builder, id_, entry):
    """
    Build an Atom feed entry.
    """
    with builder.within('entry'):
        title = entry['title']
        if title == '':
            title = 'Paste #%d' % entry['paste_id']
        builder.tag('title', title)
        link = '%s/%d' % (web.ctx.realhome, entry['paste_id'])
        builder.tag('link', rel='alternate', type='text/html', href=link)
        builder.tag('id', '%s:p%d' % (id_, entry['paste_id']))
        builder.tag('published', utils.date(entry['created']))
        builder.tag('updated', utils.date(entry['created']))
        with builder.within('author'):
            builder.tag('name', entry['poster'])
