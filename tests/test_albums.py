import requests
from api_foundry.utils.logger import logger

from test_fixtures import gateway_endpoint

log = logger(__name__)

def test_get_request_all(gateway_endpoint):
    # Define the endpoint
    endpoint = gateway_endpoint + "/album"

    log.info(f"request: {endpoint}")

    # Send the GET request
    response = requests.get(endpoint)

    # Validate the response status code
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code}"

    # Validate the response content
    albums = response.json()
    assert len(albums) == 347
    expected_keys = ["album_id", "title", "artist_id"]
    for key in expected_keys:
        assert key in albums[0], f"Missing key '{key}' in response"

    # Additional validation (if necessary)
    assert albums[0]["album_id"] == 1, "Expected 'id' to be 1"
    assert isinstance(albums[0]["title"], str), "Expected 'name' to be a string"
    assert isinstance(albums[0]["artist_id"], int), "Expected 'value' to be an integer"
