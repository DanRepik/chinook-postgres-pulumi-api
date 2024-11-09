import pytest
import subprocess
import json
from api_foundry.utils.logger import logger

log = logger(__name__)

api_id: str = None

@pytest.fixture
def gateway_endpoint():
    global api_id
    if not api_id:
        try:
            # Run Pulumi CLI command to get stack outputs as JSON
            result = subprocess.run(
                ["pulumi", "stack", "output", "--json"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the JSON output
            outputs = json.loads(result.stdout)
            log.info(f"outputs: {outputs}")
            
            # Extract the desired output
            api_id = outputs["chinook-rest-api-host"]
            log.info(f"api_id: {api_id}")
            
        except subprocess.CalledProcessError as e:
            log.error(f"Error retrieving Pulumi stack output: {e}")
            raise e
        except KeyError:
            log.error("Key 'chinook-rest-api-host' not found in Pulumi output.")
            raise KeyError("Expected output 'chinook-rest-api-host' missing in Pulumi stack output.")

    return f"http://{api_id}"
