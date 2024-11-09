import requests
import time
from api_foundry.utils.logger import logger

from test_fixtures import gateway_endpoint

log = logger(__name__)


def test_get_request_all(gateway_endpoint):
    # Define the endpoint
    endpoint = gateway_endpoint + "/album"

    log.info(f"gateway_endpoint: {gateway_endpoint}")
    log.info(f"endpoint: {endpoint}")

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
    assert albums[0] == {
        "album_id": 1,
        "artist_id": 1,
        "title": "For Those About To Rock We Salute You",
    }


def test_get_request_query_one(gateway_endpoint):
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
    assert albums[0] == {"album_id": 5, "artist_id": 3, "title": "Big Ones"}


def test_get_request_by_id(gateway_endpoint):
    # send the request
    start = time.perf_counter()
    response = requests.get(gateway_endpoint + "/album/5")
    log.info(f"response time: {time.perf_counter()-start}")

    # Validate the response
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code}"
    albums = response.json()
    assert len(albums) == 1
    assert albums[0] == {"album_id": 5, "artist_id": 3, "title": "Big Ones"}


def test_post_request(gateway_endpoint):
    # send the request
    start = time.perf_counter()
    response = requests.post(
        gateway_endpoint + "/album",
        json={"artist_id": 120, "title": "Wish You Were Here"},
    )
    log.info(f"response time: {time.perf_counter()-start}")

    # Validate the response
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code}"
    albums = response.json()
    assert len(albums) == 1
    assert "album_id" in albums[0]
    assert albums[0]["artist_id"] == 120
    assert albums[0]["title"] == "Wish You Were Here"
