HOST, PORT = '127.0.0.1', 8000

OK = 200
CREATED = 201
NO_CONTENT = 204
BAD_REQUEST = 400
FORBIDDEN = 403
SERVER_ERROR = 500
NOT_FOUND = 404
NOT_ALLOWED = 405
ACCEPTED = 202

CONTENT_TYPE = 'html'  # NOTE switch content
CONTENT_LEN_HEADER = 'Content-Length'
CONTENT_HEADER = 'Content-Type', f'text/{CONTENT_TYPE}'
ALLOW_HEADER = {'Allow': '[GET, HEAD]'}
AUTH_HEADER = 'OMDB_API_KEY'

TEMPLATES = 'templates/'
TEMPLATE_MAIN = f'{TEMPLATES}index.html'
TEMPLATE_MOVIES = f'{TEMPLATES}movies.html'
TEMPLATE_ACTORS = f'{TEMPLATES}actors.html'

YANDEX_HEADER = 'X-Yandex-API-Key'
API_URL = 'http://www.omdbapi.com/'
RATING_KEYS = 'Value'

TIMEOUT = 8

MOVIE_KEYS = ('title', 'description', 'genre', 'year', 'poster', 'trailer')
MOVIE_REQUIRED_KEYS = set(MOVIE_KEYS)