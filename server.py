from http.server import HTTPServer, BaseHTTPRequestHandler

import db
from typing import Optional
import config

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
        with open(config.TEMPLATE_MAIN, 'r') as file:
            page = file.read()
        movies = '<br>'.join(str(movie) for movie in db.get_movies(self.db_cursor))
        page_with_datetime = page.format(movies=movies)
        self.respond(config.OK, page_with_datetime)

if __name__ == '__main__':
    server = HTTPServer((config.HOST, config.PORT), MyRequestHandler)
    print(f'Server started at http://{config.HOST}:{config.PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Interrupted by user!')
    finally:
        server.server_close()