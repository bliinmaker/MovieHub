"""This module provides a web server for handling movie-related operations using http.server."""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from typing import Optional as Option
from uuid import UUID

import dotenv
import jinja2
import psycopg

import config
import db
import rating
import views

TEMPLATE_FOLDER = './templates'

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_FOLDER), autoescape=True)


def connect_my_handler(class_: type) -> type:
    """
    Dynamically injects database connection and API key into a given class.

    Args:
        class_ (type): The class to inject attributes into.

    Returns:
        type: The modified class.
    """
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
    """
    Custom request handler by Python's http.server module.

    Methods:
        get_query(self) -> dict: Extracts query parameters from the request path.
        handle_movie_rating_request(self) -> None: Processes requests for fetching movie ratings.
        respond(self, code: int, body: Optional[str] = None, headers: Optional[dict] = None) -> None.
        movies_page(self) -> None: Renders and sends the page displaying all movies.
        main_page(self) -> None: Renders and sends the main page.
        actors_page(self) -> None: Renders and sends the page displaying all actors.
        do_GET(self) -> None: Handles GET requests and routes them to the appropriate handler based on the request path.
        do_HEAD(self) -> None: Handles HEAD requests by sending an OK response.
        check_allowed(self) -> bool: Checks if the request path starts with '/movies'.
        check_auth(self) -> bool: Checks if the request contains an authorization header and if the token is valid.
        allow(self) -> bool: Checks if the request is allowed based on the path.
        auth(self) -> bool: Checks if the request is authenticated.
        allow_and_auth(self) -> bool: Combines the checks for whether the request is allowed and authenticated.
        get_json_body(self) -> dict | None: Parses the JSON body from a POST request.
        do_POST(self) -> None: Handles POST requests by processing the addition of a new movie.
        do_DELETE(self) -> None: Handles DELETE requests by processing the deletion of a movie.
        do_PUT(self) -> None: Handles PUT requests by processing the update of a movie.
    """

    def get_query(self) -> dict:
        """
        Extract query parameters from the request path.

        Returns:
            dict: A dictionary of query parameters.
        """
        query = {}
        qm_index = self.path.find('?')
        if qm_index == -1 or qm_index == len(self.path) - 1:
            return query

        for pair in self.path[qm_index + 1:].split('&'):
            key, attr = pair.split('=')
            try:
                query[key] = int(attr) if attr.isdigit() else float(attr)
            except ValueError:
                query[key] = views.plusses_to_spaces(attr)

        return query

    def handle_movie_rating_request(self) -> None:
        """Process requests for fetching movie ratings."""
        query = self.get_query()
        movie_title = query.get('title')
        movies = db.get_movies(self.db_cursor)
        if not movie_title:
            self.respond(config.BAD_REQUEST, 'Movie title is required')
            return

        try:
            movie_data = rating.get_rating(movie_title, self.apikey)
        except rating.ForeignApiError as api_error:
            self.respond(config.SERVER_ERROR, f'Failed to fetch movie details: {api_error}')
            return

        template = jinja_env.get_template('index.html')
        rendered_body = template.render(movies=movies, movie_data=movie_data)
        self.respond(config.OK, rendered_body)

    def respond(self, code: int, body: Option[str] = None, headers: Option[dict] = None) -> None:
        """
        Send an HTTP response with the specified status code and message.

        Args:
            code (int): The HTTP status code.
            body (Optional[str]): The response body. Defaults to None.
            headers (Optional[dict]): Additional headers to include in the response. Defaults to None.
        """
        self.send_response(code)
        self.send_header(*config.CONTENT_HEADER)
        if headers:
            for header_key, header_value in headers.items():
                self.send_header(header_key, header_value)
        self.end_headers()
        if body:
            self.wfile.write(body.encode())

    def movies_page(self) -> None:
        """Render and sends the page displaying all movies."""
        movies = db.get_movies(self.db_cursor)
        template = jinja_env.get_template('movies.html')
        rendered_body = template.render(movies=movies)
        self.respond(config.OK, rendered_body)

    def main_page(self) -> None:
        """Render and sends the main page."""
        movies = db.get_movies(self.db_cursor)
        template = jinja_env.get_template('index.html')
        rendered_body = template.render(movies=movies)
        self.respond(config.OK, rendered_body)

    def actors_page(self) -> None:
        """Render and sends the page displaying all actors."""
        actors = db.get_actors(self.db_cursor)
        template = jinja_env.get_template('actors.html')
        rendered_body = template.render(actors=actors)
        self.respond(config.OK, rendered_body)

    def do_GET(self) -> None:
        """Handle GET requests and routes them to the appropriate handler based on the request path."""
        if self.path.startswith('/actors'):
            self.actors_page()
        if self.path.startswith('/rating'):
            self.handle_movie_rating_request()
        elif self.path.startswith('/movies'):
            self.movies_page()
        else:
            self.main_page()

    def do_HEAD(self) -> None:
        """Handle HEAD requests by sending an OK response."""
        self.respond(config.OK)

    def check_allowed(self) -> bool:
        """
        Check if the request path starts with '/movies'.

        Returns:
            bool: True if the path starts with '/movies', False otherwise.
        """
        return self.path.startswith('/movies')

    def check_auth(self) -> bool:
        """
        Check if the request contains an authorization header and if the token is valid.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        if config.AUTH_HEADER not in self.headers.keys():
            return False
        return db.check_token(self.db_cursor, self.headers[config.AUTH_HEADER])

    def allow(self) -> bool:
        """
        Check if the request is allowed based on the path.

        Returns:
            bool: True if the request is allowed, False otherwise.
        """
        if not self.check_allowed():
            self.respond(config.NOT_ALLOWED, headers=config.ALLOW_HEADER)
            return False
        return True

    def auth(self) -> bool:
        """
        Check if the request is authenticated.

        Returns:
            bool: True if the request is authenticated, False otherwise.
        """
        if not self.check_auth():
            self.respond(config.FORBIDDEN)
            return False
        return True

    def allow_and_auth(self) -> bool:
        """
        Combine the checks for whether the request is allowed and authenticated.

        Returns:
            bool: True if both checks pass, False otherwise.
        """
        if not self.allow():
            return False
        return self.auth()

    def get_json_body(self) -> dict | None:
        """
        Parse the JSON body from a POST request.

        Returns:
            dict | None: The parsed JSON body or None if the parsing fails.
        """
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
        """Handle POST requests by processing the addition of a new movie."""
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
            self.respond(config.CREATED, body=f'{response}')
        else:
            self.respond(config.SERVER_ERROR, f'failed to create record movie={body["title"]}')

    def do_DELETE(self) -> None:
        """Handle DELETE requests by processing the deletion of a movie."""
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
        """Handle PUT requests by processing the update of a movie."""
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
    server = ThreadingHTTPServer((config.HOST, config.PORT), connect_my_handler(MyRequestHandler))
    print(f'Server started at http://{config.HOST}:{config.PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Interrupted by user!')
    finally:
        server.server_close()
