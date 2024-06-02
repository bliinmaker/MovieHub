from http.server import HTTPServer, BaseHTTPRequestHandler
import jinja2
import json
import psycopg
import db
from typing import Optional as Option
import config
import dotenv
import views
import os
import rating
from uuid import UUID

TEMPLATE_FOLDER = './templates'

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_FOLDER), autoescape=True)


def connect_my_handler(class_: type) -> type:
    dotenv.load_dotenv()
    connection, cursor = db.connect()
    attributes = {
        'apikey': os.environ.get('API_KEY'),
        'db_connection': connection,
        'db_cursor': cursor,
    }
    for name, attr in attributes.items():
        setattr(class_, name, attr)
    return class_


class MyRequestHandler(BaseHTTPRequestHandler):
    def get_query(self) -> dict:
        query = {}
        qm_index = self.path.find('?')
        if qm_index == -1 or qm_index == len(self.path) - 1:
            return query
        for pair in self.path[qm_index + 1:].split('&'):
            key, attr = pair.split('=')
            if attr.isdigit():
                query[key] = int(attr)
                continue
            try:
                float(attr)
            except ValueError:
                query[key] = views.plusses_to_spaces(attr)
            else:
                query[key] = float(attr)
        return query

    def handle_movie_rating_request(self) -> None:
        query = self.get_query()
        movie_title = query.get('title')
        movies = db.get_movies(self.db_cursor)
        print(movie_title)
        if not movie_title:
            self.respond(config.BAD_REQUEST, "Movie title is required")
            return

        try:
            movie_data = rating.get_rating(movie_title, self.apikey)
        except rating.ForeignApiError as e:
            self.respond(config.SERVER_ERROR, f"Failed to fetch movie details: {e}")
            return

        template = jinja_env.get_template('index.html')  # Используйте нужный вам шаблон
        rendered_body = template.render(movies=movies, movie_data=movie_data)
        self.respond(config.OK, rendered_body)

    def respond(self, code: int, body: Option[str] = None, headers: Option[dict] = None) -> None:
        self.send_response(code)
        self.send_header(*config.CONTENT_HEADER)
        if headers:
            for header_key, header_value in headers.items():
                self.send_header(header_key, header_value)
        self.end_headers()
        if body:
            self.wfile.write(body.encode())

    def movies_page(self) -> None:
        movies = db.get_movies(self.db_cursor)
        template = jinja_env.get_template('movies.html')
        rendered_body = template.render(movies=movies)
        self.respond(config.OK, rendered_body)

    def main_page(self) -> None:
        movies = db.get_movies(self.db_cursor)
        template = jinja_env.get_template('index.html')
        rendered_body = template.render(movies=movies)
        self.respond(config.OK, rendered_body)

    def actors_page(self) -> None:
        actors = db.get_actors(self.db_cursor)
        template = jinja_env.get_template('actors.html')
        rendered_body = template.render(actors=actors)
        self.respond(config.OK, rendered_body)

    def do_GET(self) -> None:
        if self.path.startswith('/actors'):
            self.actors_page()
        if self.path.startswith('/rating'):
            self.handle_movie_rating_request()
        elif self.path.startswith('/movies'):
            self.movies_page()
        else:
            self.main_page()

    def do_HEAD(self) -> None:
        self.respond(config.OK)

    def check_allowed(self) -> bool:
        return self.path.startswith('/movies')

    def check_auth(self) -> bool:
        if config.AUTH_HEADER not in self.headers.keys():
            return False
        return db.check_token(self.db_cursor, self.headers[config.AUTH_HEADER])

    def allow(self) -> bool:
        if not self.check_allowed():
            self.respond(config.NOT_ALLOWED, headers=config.ALLOW_HEADER)
            return False
        return True

    def auth(self) -> bool:
        if not self.check_auth():
            self.respond(config.FORBIDDEN)
            return False
        return True

    def allow_and_auth(self) -> bool:
        if not self.allow():
            return False
        return self.auth()

    def get_json_body(self) -> dict | None:
        content_len = self.headers.get(config.CONTENT_LEN_HEADER)
        if not (isinstance(content_len, str) and content_len.isdigit()):
            self.respond(config.BAD_REQUEST, f'should have provided {config.CONTENT_LEN_HEADER}')
            return None
        try:
            return json.loads(self.rfile.read(int(content_len)))
        except json.JSONDecodeError as error:
            self.respond(config.BAD_REQUEST, f'failed parsing json: {error}')
            return None

    def do_POST(self) -> None:
        if not self.allow_and_auth():
            return
        body = self.get_json_body()
        if body is None:
            return
        if set(body.keys()) != config.MOVIE_REQUIRED_KEYS:
            self.respond(config.BAD_REQUEST, f'keys {config.MOVIE_REQUIRED_KEYS} are required')
            return
        keys = [body[key] for key in config.MOVIE_KEYS]
        try:
            response = db.add_movie(self.db_cursor, self.db_connection, *keys)
        except psycopg.errors.UniqueViolation:
            self.respond(config.OK, f'record movie={body["title"]} already exists')
            self.db_connection.rollback()
            return
        if response:
            self.respond(config.CREATED, f'record with movie {body["title"]} was created')
        else:
            self.respond(config.SERVER_ERROR, f'failed to create record movie={body["title"]}')

    def do_DELETE(self) -> None:
        if not self.allow_and_auth():
            return
        query = self.get_query()
        movie_key = 'id'
        if movie_key not in query.keys():
            self.respond(config.BAD_REQUEST, 'you should have provided movie in query')
            return
        if UUID(query[movie_key]) not in db.get_movies_id(self.db_cursor):
            print(db.get_movies_id(self.db_cursor))
            self.respond(config.ACCEPTED, f'movie {query[movie_key]} is not present in database')
            return
        if db.delete_movie(self.db_cursor, self.db_connection, query[movie_key]):
            self.respond(config.NO_CONTENT)
        else:
            self.respond(config.SERVER_ERROR, f'movie {query[movie_key]} was not deleted')

    def do_PUT(self) -> None:
        if not self.allow_and_auth():
            return
        query = self.get_query()
        movie_key = 'id'
        if movie_key not in query.keys() or db.check_movie(self.db_cursor, query[movie_key]):
            self.do_POST()
            return
        movie = query[movie_key]
        body = self.get_json_body()
        for attr in body.keys():
            if attr not in config.MOVIE_REQUIRED_KEYS:
                self.respond(config.BAD_REQUEST, f'key {attr} is not defined for instance')
                return
        if db.update_movie(self.db_cursor, self.db_connection, body, movie):
            self.respond(config.OK, f'movie {movie} was updated')
        else:
            self.respond(config.SERVER_ERROR, f'movie {movie} was not updated')


if __name__ == '__main__':
    server = HTTPServer((config.HOST, config.PORT), connect_my_handler(MyRequestHandler))
    print(f'Server started at http://{config.HOST}:{config.PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Interrupted by user!')
    finally:
        server.server_close()
