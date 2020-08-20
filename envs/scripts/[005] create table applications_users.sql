CREATE TABLE application_users (
	application_id int8 NOT NULL,
	user_id int8 NOT NULL,
	id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
	CONSTRAINT application_users_pk PRIMARY KEY (id, application_id, user_id)
);

ALTER TABLE application_users 
	ADD CONSTRAINT application_user_fk FOREIGN KEY (application_id) REFERENCES applications(id);
ALTER TABLE application_users 
	ADD CONSTRAINT application_users_fk FOREIGN KEY (user_id) REFERENCES users(id);