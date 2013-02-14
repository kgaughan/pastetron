"""
Highlighting (a wrapper aroung pygments).
"""

import pygments
import pygments.lexers
import pygments.formatters


CSS_CLASS = 'highlight'

# We'll be reusing this each time something is rendered, so might as well
# create it once.
FORMATTER = pygments.formatters.HtmlFormatter(  # pylint: disable-msg=E1101
    linenos=True,
    cssclass=CSS_CLASS)


def get_stylesheet():
    """
    Generate a stylesheet for syntax highlighting the output.
    """
    return FORMATTER.get_style_defs('.' + CSS_CLASS)


def guess_lexer_alias(body):
    """
    Guess the alias of the lexer to use when rendering the given text.
    """
    return pygments.lexers.guess_lexer(body).aliases[0]


def highlight(body, syntax):
    """
    Have Pygments format the given text.
    """
    lexer = pygments.lexers.get_lexer_by_name(syntax)
    return pygments.highlight(body, lexer, FORMATTER)


def get_lexers():
    """
    For generating the lexers dropdown.
    """
    lexers = (
        (longname, aliases[0])
        for longname, aliases, _, _ in pygments.lexers.get_all_lexers()
        if len(aliases) > 0)
    return sorted(lexers, cmp=lambda x, y: cmp(x[0].lower(), y[0].lower()))


LEXERS = get_lexers()

# For converting lexer aliases to full names when rendering.
ALIAS_TO_NAME = dict((alias, longname) for longname, alias in LEXERS)
