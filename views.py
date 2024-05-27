import config
from typing import Optional


def load_page(template_path: str, params: Optional[dict] = None) -> str:
    with open(template_path, 'r') as file:
        content = file.read()
    return content.format(**params) if params else content


def movies_page(movies: list) -> str:
    return load_page(config.TEMPLATE_MOVIES, {'movies': movies_html(movies)})


def movies_html(movies: list[tuple]) -> str:
    return '\n'.join([f'<li>{movie} lat: {lat}, lon: {lon} </li>' for movie, lat, lon in movies])


def main_page() -> str:
    return load_page(config.TEMPLATE_MAIN)


def actors_page() -> str:
    return load_page(config.TEMPLATE_ACTORS)