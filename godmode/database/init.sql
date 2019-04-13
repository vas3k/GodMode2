BEGIN TRANSACTION;
CREATE TABLE gm_users (
  id INTEGER NOT NULL,
  login VARCHAR(32),
  password VARCHAR(64),
  created_at DATETIME,
  updated_at DATETIME,
  acl varchar(16) NULL,
  PRIMARY KEY (id),
  UNIQUE (login)
);
INSERT INTO gm_users VALUES(1,'demo','$2a$12$O8JP08YJU/gksIYqQpALmOlEivUDSS50UqKkSuKyWC4hU2Ae.BGtS','2015-02-18 18:23:06.000000','2015-02-18 18:23:06.000000','superuser');
CREATE TABLE gm_sessions (
  id INTEGER NOT NULL,
  user_id INTEGER,
  token VARCHAR(32),
  created_at DATETIME,
  updated_at DATETIME,
  PRIMARY KEY (id),
  FOREIGN KEY(user_id) REFERENCES gm_users (id)
);
CREATE TABLE gm_log (
  id INTEGER NOT NULL,
  "user" VARCHAR(32),
  model VARCHAR(64),
  action VARCHAR(512),
  ids VARCHAR(512),
  details VARCHAR(512),
  reason VARCHAR(64),
  created_at DATETIME,
  PRIMARY KEY (id)
);
COMMIT;


