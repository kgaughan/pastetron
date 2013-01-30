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
