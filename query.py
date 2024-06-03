"""This module contains SQL queries for interacting with a database."""

GET_MOVIES = 'select * from movie'
GET_ACTORS = 'select * from actor'
GET_TITLE_BY_MOVIE = 'select title from movie'
INSERT_MOVIE = 'insert into movie (id, title, description, genre, year, trailer, poster) values (%s, %s, %s, %s, %s, %s, %s)'
DELETE_MOVIE = 'delete from movie where id=%s'
CHECK_TOKEN = 'select count(*) from token where value=%s'
CHECK_MOVIE = 'select count(*) from movie where id=%s'
UPDATE_MOVIE = 'update movie set {params} where id=%s'
