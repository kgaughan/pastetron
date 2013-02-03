"""
Database interface code.
"""

import dbkit


@dbkit.transactional
def add_paste(poster, title, body, fmt):
    dbkit.execute("""
        INSERT INTO pastes (
            poster, title, body, syntax
        ) VALUES (
            ?, ?, ?, ?
        )
        """, (poster, title, body, fmt))
    return dbkit.last_row_id()


def get_paste(paste_id):
    return dbkit.query_row("""
        SELECT  paste_id, created, poster, title, body, syntax
        FROM    pastes
        WHERE   paste_id = ?
        """, (paste_id,))


@dbkit.transactional
def add_comment(paste_id, poster, body):
    dbkit.execute("""
        INSERT INTO comments (
            paste_id, poster, body
        ) VALUES (
            ?, ?, ?
        )
        """, (paste_id, poster, body))
    return dbkit.last_row_id()


def get_comments(paste_id):
    return dbkit.query("""
        SELECT   comment_id, paste_id, created, poster, body
        FROM     comments
        WHERE    paste_id = ?
        ORDER BY created ASC
        """, (paste_id,))
