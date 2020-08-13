CREATE TABLE application_enviroments (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    application_id bigint NOT NULL,
	"name" varchar(250) NOT NULL,
	real_name varchar(3) NOT NULL,
	description text NULL,
	created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by bigint NOT NULL,
	update_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_by bigint NOT NULL,
	CONSTRAINT application_enviroments_pk PRIMARY KEY (id),
	CONSTRAINT application_enviroments_application_fk FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
	CONSTRAINT application_enviroments_created_by_fk FOREIGN KEY (created_by) REFERENCES users(id),
	CONSTRAINT application_enviroments_updated_by_fk FOREIGN KEY (updated_by) REFERENCES users(id)
);
