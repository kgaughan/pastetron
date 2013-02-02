CREATE TABLE pastes (
	paste_id    INTEGER  NOT NULL PRIMARY KEY,
	created     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	poster      TEXT     NOT NULL DEFAULT 'Anonymous',
	body        TEXT     NOT NULL,
	syntax      TEXT     NOT NULL DEFAULT 'text'
);

CREATE INDEX ix_paste_created ON pastes (created);

CREATE TABLE comments (
	comment_id INTEGER  NOT NULL PRIMARY KEY,
	paste_id   INTEGER  NOT NULL REFERENCES pastes (paste_id),
	created    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	poster     TEXT     NOT NULL DEFAULT 'Anonymous',
	body       TEXT     NOT NULL
);

CREATE INDEX ix_comment_paste ON comments (paste_id);
