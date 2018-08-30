DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

INSERT INTO user (username, password) VALUES
  ('spolonus282@gmail.com','pbkdf2:sha256:50000$9e9wG9mr$2150c4eb90032b614025c99d194912bf758784126bc7a9ac005276b4bf443e54'),
  ('squidmanwizard@gmail.com','pbkdf2:sha256:50000$grnkmZxr$57a8c99ca30b655991ec417743ac6689a681272e4aefc1cdbf125c893ea01d85'),
  ('epolonus@hotmail.com','pbkdf2:sha256:50000$tXHyLZ6P$633856b72486005dc64f7927da3c9d78f474d62c3fce9f2c79f94b1b1e1b7ff5'),
  ('kpolonus@hotmail.com','pbkdf2:sha256:50000$3tWSpU9L$9deb24ac24b1fa8c11de131a487cd8120f0325a2724e80f2f70127b43b34d65c');
