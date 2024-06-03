"""This module provides functions for rendering views using templates."""

from typing import Optional

import config


def load_template(template_path: str, template_params: Optional[dict] = None) -> str:
    """
    Load and format a template page with given parameters.

    Args:
        template_path (str): Path to the template file.
        template_params (Optional[dict], optional): Dictionary of parameters for formatting the template. Defaults None.

    Returns:
        str: Formatted content of the template.
    """
    with open(template_path, 'r') as template_file:
        formatted_content = template_file.read()
    return formatted_content.format(**template_params) if template_params else formatted_content


def movies_page(movies: list) -> str:
    """
    Render a page displaying a list of movies.

    Args:
        movies (list): List of movies to display.

    Returns:
        str: HTML string representing the movies page.
    """
    return load_template(config.TEMPLATE_MOVIES, {'movies': movies})


def main_page(movies: list) -> str:
    """
    Render the main page displaying a list of movies.

    Args:
        movies (list): List of movies to display on the main page.

    Returns:
        str: HTML string representing the main page.
    """
    return load_template(config.TEMPLATE_MAIN, {'movies': movies})


def actors_page(actors: list[tuple]) -> str:
    """
    Render a page displaying a list of actors.

    Args:
        actors (list[tuple]): List of tuples (actor name, photo URL) to display.

    Returns:
        str: HTML string representing the actors page.
    """
    return load_template(config.TEMPLATE_ACTORS, {'actors': actors})


def plusses_to_spaces(text: str) -> str:
    """
    Replace spaces in the text with '+'.

    Args:
        text (str): Input text.

    Returns:
        str: Text with replaced spaces by '+'.
    """
    return text.replace(' ', '+')


def replace_plus_signs_with_spaces(text: str) -> str:
    """
    Replace '+' characters in the text with spaces.

    Args:
        text (str): Input text.

    Returns:
        str: Text with replaced '+' characters by spaces.
    """
    return text.replace('+', ' ')
