CREATE TABLE pastes (
	paste_id    INTEGER  NOT NULL PRIMARY KEY,
	created     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	name        TEXT     NOT NULL,
	description TEXT     NOT NULL,
	body        TEXT     NOT NULL
);

CREATE INDEX ix_paste_created ON pastes (created);

CREATE TABLE comments (
	comment_id INTEGER  NOT NULL PRIMARY KEY,
	paste_id   INTEGER  NOT NULL DEFAULT 0 REFERENCES pastes (paste_id),
	created    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	comment    TEXT     NOT NULL
);

CREATE TABLE users (
	user_id  INTEGER NOT NULL PRIMARY KEY,
	username TEXT    NOT NULL,
	email    TEXT    NULL
);

CREATE UNIQUE INDEX ux_user_username ON users (username);
