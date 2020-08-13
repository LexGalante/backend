CREATE TABLE applications (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
	"name" varchar(250) NOT NULL,
	"type" smallint NOT NULL,
	description varchar(250) NOT NULL,
	details text NULL,
	created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by bigint NOT NULL,
	updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_by bigint NOT NULL,
	active bool NULL DEFAULT TRUE,
	CONSTRAINT applications_pk PRIMARY KEY (id),
	CONSTRAINT applications_check CHECK ((type IN(1, 2, 3)))
);

CREATE INDEX applications_active_idx ON applications (active);

ALTER TABLE applications
    ADD CONSTRAINT aplications_created_by_fk FOREIGN KEY(created_by) REFERENCES users(id)

ALTER TABLE applications
    ADD CONSTRAINT aplications_updated_by_fk FOREIGN KEY(updated_by) REFERENCES users(id)
