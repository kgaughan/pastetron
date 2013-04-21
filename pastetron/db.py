"""
Database interface code.
"""

import dbkit

from pastetron import utils


@dbkit.transactional
def add_paste(poster, title, chunks):
    """
    Create a new paste.
    """
    dbkit.execute("""
        INSERT INTO pastes (poster, title) VALUES (?, ?)
        """, (poster, title))
    paste_id = dbkit.last_row_id()
    for body, syntax in chunks:
        dbkit.execute("""
            INSERT INTO chunks (paste_id, body, syntax) VALUES (?, ?, ?)
            """, (paste_id, body, syntax))
    return paste_id


def get_paste(paste_id):
    """
    Get a paste by ID.
    """
    paste = dbkit.query_row("""
        SELECT  paste_id, created, poster, title
        FROM    pastes
        WHERE   paste_id = ?
        """, (paste_id,))
    if paste is not None:
        paste['chunks'] = dbkit.query("""
            SELECT  chunk_id, body, syntax
            FROM    chunks
            WHERE   paste_id = ?
            ORDER BY chunk_id
            """, (paste_id,))
    return paste


def get_chunk(chunk_id):
    """
    Get a paste chunk by ID.
    """
    return dbkit.query_row("""
        SELECT  body, syntax
        FROM    chunks
        WHERE   chunk_id = ?
        """, (chunk_id,))


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
    return utils.to_page_count(
        dbkit.query_value("""
            SELECT  COUNT(*)
            FROM    pastes
            """),
        utils.get_page_length())


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
        SELECT   paste_id, title, created, poster
        FROM     pastes
        ORDER BY created DESC
        LIMIT    ?
        """, (utils.get_page_length(),))
