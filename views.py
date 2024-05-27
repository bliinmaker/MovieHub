import config
from typing import Optional

def load_page(template_path: str, params: Optional[dict] = None) -> str:
    with open(template_path, 'r') as file:
        content = file.read()
    return content.format(**params) if params else content


def movies_page(movies: tuple) -> str:
    return load_page(config.TEMPLATE_MOVIES, {'movies': str(movies)})