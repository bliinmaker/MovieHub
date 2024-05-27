from http.server import HTTPServer, BaseHTTPRequestHandler

import db
from typing import Optional
import config
import views

class MyRequestHandler(BaseHTTPRequestHandler):
    db_connection, db_cursor = db.connect()

    def respond(self,
                status: int,
                body: Optional[str] = None,
                headers: Optional[dict] = None,
                ) -> None:
        self.send_response(status)
        self.send_header(*config.CONTENT_HEADER)
        if headers:
            for header_key, value in headers.items():
                self.send_header(header_key, value)
        self.end_headers()
        self.wfile.write(body.encode())

    def do_GET(self) -> None:
        movies = db.get_movies(self.db_cursor)
        self.respond(config.OK, views.movies_page(movies))

if __name__ == '__main__':
    server = HTTPServer((config.HOST, config.PORT), MyRequestHandler)
    print(f'Server started at http://{config.HOST}:{config.PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Interrupted by user!')
    finally:
        server.server_close()