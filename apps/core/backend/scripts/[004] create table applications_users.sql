CREATE TABLE applications_users (
	application_id bigint NOT NULL,
	user_id bigint NOT NULL,
	created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_by bigint NOT NULL,
	CONSTRAINT applications_users_pk PRIMARY KEY (application_id,user_id)
);

ALTER TABLE applications_users
    ADD CONSTRAINT applications_users_application_fk FOREIGN KEY(application_id) REFERENCES applications(id)

ALTER TABLE applications_users
    ADD CONSTRAINT applications_users_user_fk FOREIGN KEY(user_id) REFERENCES user(id)
