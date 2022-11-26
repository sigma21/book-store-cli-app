-- This script was generated by a beta version of the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public."Book"
(
    id serial,
    name character varying,
    author character varying,
    page integer,
    genre character varying,
    available_quantity integer,
    total_quantity integer,
    date_added TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."User"
(
    username character varying,
    password character varying,
    fav_authors character varying[],
    PRIMARY KEY (username)
);

CREATE TABLE IF NOT EXISTS public."User_Book"
(
    book serial,
    "user" character varying,
    read boolean,
    fav boolean
);

ALTER TABLE IF EXISTS public."User_Book"
    ADD FOREIGN KEY (book)
    REFERENCES public."Book" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."User_Book"
    ADD FOREIGN KEY ("user")
    REFERENCES public."User" (username) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;