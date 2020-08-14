ALTER TABLE application_enviroments ALTER COLUMN real_name TYPE varchar(250) USING real_name::varchar;
ALTER TABLE application_enviroments ALTER COLUMN "name" TYPE varchar(3) USING "name"::varchar;
