"""
Database interface code.
"""

import dbkit


@dbkit.transactional
def add_paste(poster, body, fmt):
    dbkit.execute("""
        INSERT INTO pastes (
            poster, body, format
        ) VALUES (
            ?, ?, ?
        )
        """, (poster, body, fmt))
    return dbkit.last_row_id()


def get_paste(paste_id):
    return dbkit.query_row("""
        SELECT  paste_id, created, poster, body, format
        FROM    pastes
        WHERE   paste_id = ?
        """, (paste_id,))
