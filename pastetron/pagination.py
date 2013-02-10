"""
Pagination support code.
"""


BUFFER = 5


def paginator(page_num, max_page, buffer_size=BUFFER):
    """
    Pagination generator.

    Generates a sequence of page numbers, giving the pages at the beginning
    and end, and around the current page, with a number of buffer pages on
    each side of both. Omitted pages in the sequence are elided into a `None`.
    """
    if page_num - buffer_size > 1:
        yield 1
    if page_num - buffer_size > 2:
        yield None
    begin = max(1, page_num - buffer_size)
    end = min(max_page, page_num + buffer_size)
    for i in xrange(begin, end + 1):
        yield i
    if max_page - page_num - buffer_size > 1:
        yield None
    if max_page - page_num - buffer_size > 0:
        yield max_page
