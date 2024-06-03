"""Tests REST API endpoints for movie management."""

import pytest
import requests

from config import AUTH_HEADER, CREATED, NO_CONTENT, OK

HEADERS = {AUTH_HEADER: '5720906c'}
BASE_URL = 'http://localhost:8080/movies'

TEST_MOVIE_CREATE = {
    'title': 'Супер филм?!',
    'description': 'Описание нevового фильма',
    'genre': 'Драма',
    'year': 2024,
    'poster': 'url_постера',
    'trailer': 'url_trailer',
}

TEST_MOVIE_UPDATE = {
    'title': 'Супер-пупер-дупер филм!!',
    'description': 'Описание нового фильма',
    'genre': 'Драма',
    'year': 2024,
    'poster': 'url_постера',
    'trailer': 'url_trailer',
}

TEST_ID = ''
TEST_MOVIE = ((TEST_MOVIE_CREATE, TEST_MOVIE_UPDATE), )


@pytest.mark.parametrize('model_data, model_data_update', TEST_MOVIE)
def test_crud_movie(model_data, model_data_update):
    """
    Test methods for movies: creation, retrieval, update, and deletion.

    Args:
        model_data (dict): Data representing a new movie to be created.
        model_data_update (dict): Data representing the updated version of the movie.
    """
    response = requests.post(BASE_URL, headers=HEADERS, json=model_data)
    film_id = response.content.decode()
    assert response.status_code == CREATED
    url = f'{BASE_URL}?id={film_id}'

    response = requests.get(BASE_URL)
    assert response.status_code == OK

    response = requests.put(url, headers=HEADERS, json=model_data_update)
    assert response.status_code == OK

    response = requests.delete(url, headers=HEADERS)
    assert response.status_code == NO_CONTENT
