import psycopg
import dotenv
import os
import query
from uuid import UUID, uuid4


def connect() -> tuple[psycopg.Connection, psycopg.Cursor]:
    dotenv.load_dotenv()
    port = os.environ.get('PG_PORT')
    credentials = {
        'host': os.environ.get('PG_HOST', default='127.0.0.1'),
        'port': int(port) if port.isdigit() else 5555,
        'dbname': os.environ.get('PG_DBNAME', default='test'),
        'user': os.environ.get('PG_USER', default='test'),
        'password': os.environ.get('PG_PASSWORD'),
    }
    connection = psycopg.connect(**credentials)
    cursor = connection.cursor()
    return connection, cursor


def get_movies(cursor: psycopg.Cursor) -> list[tuple]:
    cursor.execute(query.GET_MOVIES)
    movies = cursor.fetchall()
    return movies


def get_actors(cursor: psycopg.Cursor) -> list[tuple]:
    cursor.execute(query.GET_ACTORS)
    actors = cursor.fetchall()
    return actors


def get_movies_id(cursor: psycopg.Cursor) -> list[str]:
    cursor.execute(query.GET_MOVIES)
    return [row[6] for row in cursor.fetchall()]


def get_coords_by_movie(cursor: psycopg.Cursor, title: str) -> tuple:
    cursor.execute(query.GET_COORDS_BY_MOVIE, params=(title,))
    return cursor.fetchone()


def change_db(
    cursor: psycopg.Cursor, conn: psycopg.Connection,
    db_query: str, query_params: tuple,
) -> bool:
    cursor.execute(db_query, params=query_params)
    conn.commit()
    return bool(cursor.rowcount)


def add_movie(
    cursor: psycopg.Cursor, conn: psycopg.Connection,
    title: str, description: str, genre: str, year: int, trailer: str, poster: str
) -> bool:
    return change_db(cursor, conn, query.INSERT_MOVIE, (uuid4(), title, description, genre, year, trailer, poster))


def delete_movie(
    cursor: psycopg.Cursor, conn: psycopg.Connection,
    id: UUID,
) -> bool:
    return change_db(cursor, conn, query.DELETE_MOVIE, (id,))


def update_params(new_attrs: list) -> str:
    return ', '.join(f'{attr}=%s' for attr in new_attrs)


def update_movie(
    cursor: psycopg.Cursor, conn: psycopg.Connection,
    new_attrs: dict, id: UUID,
) -> bool:
    query_params, values_params = [], []
    for attr, new_value in new_attrs.items():
        query_params.append(attr)
        values_params.append(new_value)
    values_params.append(id)
    query_update = query.UPDATE_MOVIE.format(params=update_params(query_params))
    cursor.execute(query_update, params=values_params)
    conn.commit()
    return bool(cursor.rowcount)


def check_token(cursor: psycopg.Cursor, token: str) -> bool:
    cursor.execute(query.CHECK_TOKEN, params=(token,))
    return bool(cursor.fetchone()[0])


def check_movie(cursor: psycopg.Cursor, movie: str) -> bool:
    cursor.execute(query.CHECK_TOKEN, params=(movie,))
    return bool(cursor.fetchone()[0])