import config
from typing import Optional


def load_page(template_path: str, params: Optional[dict] = None) -> str:
    with open(template_path, 'r') as file:
        content = file.read()
    return content.format(**params) if params else content


def movies_page(movies: list) -> str:
    return load_page(config.TEMPLATE_MOVIES, {'movies': movies})


def main_page(movies: list) -> str:
    return load_page(config.TEMPLATE_MAIN, {'movies': movies})


def actors_page(actors: list[tuple]) -> str:
    return load_page(config.TEMPLATE_ACTORS, {'actors': actors})


def spaces_to_plusses(text: str) -> str:
    return text.replace(' ', '+')


def plusses_to_spaces(text: str) -> str:
    return text.replace('+', ' ')