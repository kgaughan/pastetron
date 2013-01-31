"""
Highlighting (a wrapper aroung pygments).
"""

import pygments
import pygments.lexers
import pygments.formatters


# for generating the lexers dropdown.
LEXERS = [('Guess', '')] + sorted(
    (longname, aliases[0])
    for longname, aliases, _, _ in pygments.lexers.get_all_lexers()
    if len(aliases) > 0)

# For converting lexer aliases to full names when rendering.
ALIAS_TO_NAME = dict((alias, longname) for longname, alias in LEXERS)

# We'll be reusing this each time something is rendered, so might as well
# create it once.
FORMATTER = pygments.formatters.HtmlFormatter(
    linenos=True,
    cssclass='highlight')


def get_stylesheet():
    """
    Generate a stylesheet for syntax highlighting the output.
    """
    return FORMATTER.get_style_defs('.highlight')


def guess_lexer_alias(body):
    """
    Guess the alias of the lexer to use when rendering the given text.
    """
    return pygments.lexers.guess_lexer(body).aliases[0]


def highlight(body, format):
    """
    Have Pygments format the given text.
    """
    lexer = pygments.lexers.get_lexer_by_name(format)
    return pygments.highlight(body, lexer, FORMATTER)
