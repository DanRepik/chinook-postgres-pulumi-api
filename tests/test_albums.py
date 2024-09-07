import requests
import time
from api_foundry.utils.logger import logger

from test_fixtures import gateway_endpoint

log = logger(__name__)

def test_get_request_all(gateway_endpoint):
    # Define the endpoint
    endpoint = gateway_endpoint + "/album"

    log.info(f"request: {endpoint}")

    # Send the GET request
    start = time.perf_counter()
    response = requests.get(endpoint)
    log.info(f"response time: {time.perf_counter()-start}")

    # Validate the response status code
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code}"

    # Validate the response content
    albums = response.json()
    assert len(albums) == 347
    assert albums[0] == {'album_id': 1,
        'artist_id': 1,
        'title': 'For Those About To Rock We Salute You'
    }

def test_get_request_one(gateway_endpoint):
    # Define the endpoint
    endpoint = gateway_endpoint + "/album?album_id=5"

    log.info(f"request: {endpoint}")

    # Send the GET request
    start = time.perf_counter()
    response = requests.get(endpoint)
    log.info(f"response time: {time.perf_counter()-start}")

    # Validate the response status code
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code}"

    # Validate the response content
    albums = response.json()
    assert len(albums) == 1
    assert albums[0] == {'album_id': 5, 'artist_id': 3, 'title': 'Big Ones'}
    