"""A module to fetch movie ratings from OMDB using an API key."""

import json

import requests

from config import API_URL, OK, TIMEOUT


class ForeignApiError(Exception):
    """Custom exception raised when an external API call fails."""

    def __init__(self, api_name: str, status_code: int) -> None:
        """
        Initialize the ForeignApiError exception with the name of the API and the status code.

        Args:
            api_name (str): Name of the API that failed.
            status_code (int): Status code received from the API.
        """
        super().__init__(f'API {api_name} failed with status code {status_code}')


def get_rating(title: str, apikey: str) -> dict:
    """
    Fetch movie ratings from OMDB based on title and API key.

    Args:
        title (str): Title of the movie to fetch ratings for.
        apikey (str): API key required for accessing OMDB.

    Returns:
        dict: Dictionary containing movie ratings.

    Raises:
        ForeignApiError: If the OMDB API call fails.
    """
    url = f'{API_URL}?apikey={apikey}&t={title}'
    response = requests.get(url, timeout=TIMEOUT)
    if response.status_code != OK:
        raise ForeignApiError('OMDB.Ratings', response.status_code)
    return json.loads(response.content)
