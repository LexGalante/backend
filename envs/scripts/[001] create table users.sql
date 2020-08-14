CREATE TABLE users (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
	email varchar(250) NOT NULL,
	"password" varchar(150) NOT NULL,
	active bool NOT NULL DEFAULT true,
	CONSTRAINT users_pk PRIMARY KEY (id),
	CONSTRAINT users_un UNIQUE (email)
)

CREATE INDEX users_email_idx ON users (email)
