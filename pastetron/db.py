"""
Database interface code.
"""

import dbkit

from pastetron import utils


@dbkit.transactional
def add_paste(poster, title, body, fmt):
    """
    Create a new paste.
    """
    dbkit.execute("""
        INSERT INTO pastes (
            poster, title, body, syntax
        ) VALUES (
            ?, ?, ?, ?
        )
        """, (poster, title, body, fmt))
    return dbkit.last_row_id()


def get_paste(paste_id):
    """
    Get a paste by ID.
    """
    return dbkit.query_row("""
        SELECT  paste_id, created, poster, title, body, syntax
        FROM    pastes
        WHERE   paste_id = ?
        """, (paste_id,))


@dbkit.transactional
def add_comment(paste_id, poster, body):
    """
    Attach a comment to a paste.
    """
    dbkit.execute("""
        INSERT INTO comments (
            paste_id, poster, body
        ) VALUES (
            ?, ?, ?
        )
        """, (paste_id, poster, body))
    return dbkit.last_row_id()


def get_comments(paste_id):
    """
    Get the comments attached to a paste.
    """
    return dbkit.query("""
        SELECT   comment_id, paste_id, created, poster, body
        FROM     comments
        WHERE    paste_id = ?
        ORDER BY created ASC
        """, (paste_id,))


def get_page_count():
    """
    Get number of pages needed to list all pastes.
    """
    n_pastes = dbkit.query_value("SELECT COUNT(*) FROM pastes")
    if n_pastes == 0:
        return 0
    return (n_pastes / utils.get_page_length()) + 1


def get_paste_list(page):
    """
    Get the list of pastes for the given page.
    """
    start = (page - 1) * utils.get_page_length()
    return dbkit.query("""
        SELECT   paste_id, title, poster, created
        FROM     pastes
        ORDER BY created DESC
        LIMIT    ?, ?
        """, (start, utils.get_page_length()))


def get_latest_pastes():
    """
    Get the most recently posted pastes.
    """
    return dbkit.query("""
        SELECT   paste_id, title, created, poster, body
        FROM     pastes
        ORDER BY created DESC
        LIMIT    ?
        """, (utils.get_page_length(),))
