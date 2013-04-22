CREATE TABLE pastes (
	paste_id    INTEGER  NOT NULL PRIMARY KEY,
	created     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	poster      TEXT     NOT NULL DEFAULT 'Anonymous',
	user_id     INTEGER  NULL REFERENCES users (user_id),
	title       TEXT     NOT NULL
);

CREATE INDEX ix_paste_created ON pastes (created);
CREATE INDEX ix_paste_creator ON pastes (user_id);

CREATE TABLE chunks (
	chunk_id    INTEGER  NOT NULL PRIMARY KEY,
	paste_id    INTEGER  NULL REFERENCES pastes (paste_id),
	body        TEXT     NOT NULL,
	syntax      TEXT     NOT NULL DEFAULT 'text'
);

CREATE INDEX ix_chunk_paste ON chunks (paste_id);

CREATE TABLE comments (
	comment_id INTEGER  NOT NULL PRIMARY KEY,
	paste_id   INTEGER  NOT NULL REFERENCES pastes (paste_id),
	created    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	poster     TEXT     NOT NULL DEFAULT 'Anonymous',
	user_id    INTEGER  NULL REFERENCES users (user_id),
	body       TEXT     NOT NULL
);

CREATE INDEX ix_comment_paste ON comments (paste_id);
CREATE INDEX ix_comment_creator ON comments (user_id);

CREATE TABLE users (
	user_id      INTEGER NOT NULL PRIMARY KEY,
	username     TEXT    NOT NULL,
	password     TEXT    NULL,
	display_name TEXT    NOT NULL,
	email        TEXT    NULL
);

CREATE UNIQUE INDEX ux_user_username ON users (username);
