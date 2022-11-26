-- This script was generated by a beta version of the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public."Book"
(
    book_id serial,
    name character varying,
    author character varying,
    page integer,
    genre character varying,
    available_quantity integer,
    total_quantity integer,
    date_added TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (book_id)
);

CREATE TABLE IF NOT EXISTS public."Users"
(
    username character varying,
    PRIMARY KEY (username)
);

CREATE TABLE IF NOT EXISTS public."User_Book"
(
    id serial,
    book_id integer,
    username character varying,
    reading_status character varying,
    is_fav boolean,
    borrowed_amount integer,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public."User_Book"
    ADD FOREIGN KEY (book_id)
    REFERENCES public."Book" (book_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."User_Book"
    ADD FOREIGN KEY (username)
    REFERENCES public."Users" (username) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;