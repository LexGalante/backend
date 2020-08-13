CREATE TABLE application_features (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
	"name" varchar(250) NOT NULL,
	"enable" bool NOT NULL DEFAULT false,
	created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by bigint NOT NULL,
	updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_by bigint NOT NULL,
	application_id bigint NOT NULL,
	CONSTRAINT application_features_pk PRIMARY KEY (id),
	CONSTRAINT application_features_un UNIQUE ("name")
);

ALTER TABLE application_features
    ADD CONSTRAINT application_features_application_fk FOREIGN KEY(application_id) REFERENCES applications(id)

ALTER TABLE application_features
    ADD CONSTRAINT application_features_created_by_fk FOREIGN KEY(created_by) REFERENCES users(id)

ALTER TABLE application_features
    ADD CONSTRAINT application_features_updated_by_fk FOREIGN KEY(updated_by) REFERENCES users(id)
