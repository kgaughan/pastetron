"""
Pagination support code.
"""


BUFFER = 5


def paginator(page_num, max_page, buffer_size=BUFFER):
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
