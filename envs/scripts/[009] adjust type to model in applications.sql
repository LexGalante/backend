ALTER TABLE applications RENAME COLUMN "type" TO model;
ALTER TABLE applications DROP CONSTRAINT applications_check
ALTER TABLE public.applications ADD CONSTRAINT applications_check CHECK ((model = ANY (ARRAY[1, 2, 3])))