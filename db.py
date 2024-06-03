"""A module providing utility functions for interacting with a PostgreSQL database."""

import os
from uuid import UUID, uuid4

import dotenv
import psycopg

import query

DEFAULT_PG_PORT = 5555


def connect() -> tuple[psycopg.Connection, psycopg.Cursor]:
    """
    Establish a connection to the PostgreSQL database and returns a cursor object.

    Returns:
        A tuple containing a psycopg.Connection object and a psycopg.Cursor object.
    """
    dotenv.load_dotenv()
    port = os.environ.get('PG_PORT')
    credentials = {
        'host': os.environ.get('PG_HOST', default='127.0.0.1'),
        'port': int(port) if port.isdigit() else DEFAULT_PG_PORT,
        'dbname': os.environ.get('PG_DBNAME', default='test'),
        'user': os.environ.get('PG_USER', default='test'),
        'password': os.environ.get('PG_PASSWORD'),
    }
    connection = psycopg.connect(**credentials)
    cursor = connection.cursor()
    return connection, cursor


def get_movies(cursor: psycopg.Cursor) -> list[tuple]:
    """
    Fetch all movies from the database.

    Parameters:
        cursor: The database cursor object to execute the query.

    Returns:
        A list of tuples representing movie records.
    """
    cursor.execute(query.GET_MOVIES)
    return cursor.fetchall()


def get_actors(cursor: psycopg.Cursor) -> list[tuple]:
    """
    Fetch all actors from the database.

    Parameters:
        cursor: The database cursor object to execute the query.

    Returns:
        A list of tuples representing actor records.
    """
    cursor.execute(query.GET_ACTORS)
    return cursor.fetchall()


def get_movies_id(cursor: psycopg.Cursor) -> list[str]:
    """
    Fetch movie IDs from the database.

    Parameters:
        cursor: The database cursor object to execute the query.

    Returns:
        A list of movie IDs.
    """
    cursor.execute(query.GET_MOVIES)
    return [row[6] for row in cursor.fetchall()]


def get_coords_by_movie(cursor: psycopg.Cursor, title: str) -> tuple:
    """
    Fetch coordinates associated with a given movie title from the database.

    Parameters:
        cursor: The database cursor object to execute the query.
        title: The title of the movie to fetch coordinates for.

    Returns:
        A tuple containing the coordinates for the specified movie, or None if not found.
    """
    cursor.execute(query.GET_COORDS_BY_MOVIE, params=(title,))
    return cursor.fetchone()


def change_db(
    cursor: psycopg.Cursor, conn: psycopg.Connection,
    db_query: str, query_params: tuple,
) -> bool:
    """
    Execute a given SQL query with provided parameters and commits the changes to the database.

    Parameters:
        cursor: The database cursor object to execute the query.
        conn: The database connection object to commit the transaction.
        db_query: The SQL query string to be executed.
        query_params: A tuple of parameters to be passed to the query.

    Returns:
        True if the query execution was successful, False otherwise.
    """
    cursor.execute(db_query, params=query_params)
    conn.commit()
    return bool(cursor.rowcount)


def add_movie(
    cursor: psycopg.Cursor, conn: psycopg.Connection,
    title: str, description: str, genre: str, year: int, trailer: str, poster: str,
) -> UUID | bool:
    """
    Add a new movie entry to the database with the provided details.

    Parameters:
        cursor: The database cursor object to execute the insert query.
        conn: The database connection object to commit the transaction.
        title: The title of the movie.
        description: A brief description of the movie.
        genre: The genre(s) of the movie.
        year: The release year of the movie.
        trailer: The URL of the movie's trailer.
        poster: The URL of the movie's poster image.

    Returns:
        True if the movie was successfully added, False otherwise.
    """
    movie_id = uuid4()
    is_upd = change_db(cursor, conn, query.INSERT_MOVIE, (movie_id, title, description, genre, year, trailer, poster))
    if is_upd:
        return movie_id
    return False


def delete_movie(
    cursor: psycopg.Cursor, conn: psycopg.Connection,
    movie_id: UUID,
) -> bool:
    """
    Delete a movie entry from the database based on its ID.

    Parameters:
        cursor: The database cursor object to execute the delete query.
        conn: The database connection object to commit the transaction.
        movie_id: The unique identifier of the movie to be deleted.

    Returns:
        True if the movie was successfully deleted, False otherwise.
    """
    return change_db(cursor, conn, query.DELETE_MOVIE, (movie_id,))


def update_params(new_attrs: list) -> str:
    """
    Construct a string of parameter placeholders for a SQL query based on the provided attributes.

    Parameters:
        new_attrs: A list of attribute names to be included in the query.

    Returns:
        A string of attribute placeholders separated by commas.
    """
    return ', '.join(f'{attr}=%s' for attr in new_attrs)


def update_movie(
    cursor: psycopg.Cursor, conn: psycopg.Connection,
    new_attrs: dict, movie_id: UUID,
) -> bool:
    """
    Update an existing movie entry in the database with new attributes.

    Parameters:
        cursor: The database cursor object to execute the update query.
        conn: The database connection object to commit the transaction.
        new_attrs: A dictionary mapping attribute names to their new values.
        movie_id: The unique identifier of the movie to be updated.

    Returns:
        True if the movie was successfully updated, False otherwise.
    """
    query_params, values_params = [], []
    for attr, new_value in new_attrs.items():
        query_params.append(attr)
        values_params.append(new_value)
    values_params.append(movie_id)
    query_update = query.UPDATE_MOVIE.format(params=update_params(query_params))
    cursor.execute(query_update, params=values_params)
    conn.commit()
    return bool(cursor.rowcount)


def check_token(cursor: psycopg.Cursor, token: str) -> bool:
    """
    Check if a given token exists in the database.

    Parameters:
        cursor: The database cursor object to execute the query.
        token: The token to be checked.

    Returns:
        True if the token exists, False otherwise.
    """
    cursor.execute(query.CHECK_TOKEN, params=(token,))
    return bool(cursor.fetchone()[0])


def check_movie(cursor: psycopg.Cursor, movie: str) -> bool:
    """
    Check if a given movie title exists in the database.

    Parameters:
        cursor: The database cursor object to execute the query.
        movie: The title of the movie to be checked.

    Returns:
        True if the movie exists, False otherwise.
    """
    cursor.execute(query.CHECK_TOKEN, params=(movie,))
    return bool(cursor.fetchone()[0])
