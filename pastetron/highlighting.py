"""
Highlighting (a wrapper aroung pygments).
"""

import cgi
import contextlib
import creole
import csv
import pygments
import pygments.lexers
import pygments.formatters
try:
    import cStringIO as stringio
except:  # pylint: disable-msg=W0702
    import StringIO as stringio


CSS_CLASS = 'highlight'

# We'll be reusing this each time something is rendered, so might as well
# create it once.
FORMATTER = pygments.formatters.HtmlFormatter(  # pylint: disable-msg=E1101
    linenos=True,
    cssclass=CSS_CLASS)


def guess_lexer_alias(body):
    """
    Guess the alias of the lexer to use when rendering the given text.
    """
    return pygments.lexers.guess_lexer(body).aliases[0]


def csv_to_html(body):
    """
    Convert a CSV file to HTML.
    """
    def to_cells(tag, line):
        """
        Convert a line of a CSV file to HTML.
        """
        return ''.join(
            '<%(tag)s>%(value)s</%(tag)s>' % {
                'tag': tag,
                'value': cgi.escape(value)
            }
            for value in line)

    with contextlib.closing(stringio.StringIO()) as out:
        out.write('<table class="csv"><thead>')
        tag = 'th'
        for line in csv.reader(body.splitlines()):
            out.write('<tr>')
            out.write(to_cells(tag, line))
            out.write('</tr>')
            if tag == 'th':
                out.write('</thead></tbody>')
                tag = 'td'
        out.write('</table>')
        return out.getvalue()


def highlight(body, syntax):
    """
    Have Pygments format the given text.
    """
    if syntax == 'creole':
        return '<div class="creole">%s</div>' % (
            creole.creole2html(body, blog_line_breaks=False),
        )
    if syntax == 'csv':
        return csv_to_html(body)
    lexer = pygments.lexers.get_lexer_by_name(syntax)
    return pygments.highlight(body, lexer, FORMATTER)


def get_lexers():
    """
    For generating the lexers dropdown.
    """
    lexers = (
        (longname, aliases[0])
        for longname, aliases, _, _ in pygments.lexers.get_all_lexers()
        if len(aliases) > 0 and aliases[0] not in ('text',))
    return [
        ('Text only', 'text'),
        ('Creole markup (rendered)', 'creole'),
        ('CSV data (rendered)', 'csv'),
    ] + sorted(lexers, cmp=lambda x, y: cmp(x[0].lower(), y[0].lower()))


LEXERS = get_lexers()

# For converting lexer aliases to full names when rendering.
ALIAS_TO_NAME = dict((alias, longname) for longname, alias in LEXERS)
